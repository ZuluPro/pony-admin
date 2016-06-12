import os
from django.contrib.admin.options import csrf_protect_m
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from pony_admin.admin import BaseAdmin, ChangeList
from pony_admin.storage.forms import FileAddForm


class StorageAdmin(BaseAdmin):
    list_display = ['get_url_link']
    change_list_template = 'pony_admin/storage/changelist.html'
    change_form = FileAddForm
    actions = ['delete_selected']

    def get_objects(self, request):
        path = request.GET.get('path', '')
        objs = self.model.storage.listdir(path)
        dirs = [{'type': 'directory', 'name': name,
                 'url': self.model.storage.url(os.path.join(path, name)),
                 'path': os.path.join(path, name)}
                for name in objs[0]]
        files = [{'type': 'file', 'name': name,
                  'url': self.model.storage.url(os.path.join(path, name)),
                  'path': os.path.join(path, name)}
                 for name in objs[1]]
        return dirs + files

    def get_url_link(self, obj):
        if obj['type'] == 'directory':
            return '<a href="?path={path}">{name}/</a>'.format(**obj)
        return '<a href="{url}">{name}</a>'.format(**obj)
    get_url_link.allow_tags = True
    get_url_link.short_description = 'URL'

    def _get_changelist_context(self, request):
        path = request.GET.get('path', '')
        paths = []
        # Create breadcrumbs
        if path:
            path_ = path
            while path_:
                dir_path, file_path = os.path.split(path_)
                paths.append([path_, file_path])
                path_ = dir_path
        return {
            'path': path,
            'storage': self.model.storage,
            'files': self.get_objects(request),
            'paths': paths[::-1]
        }

    def _add(self, form):
        self.model.storage.save(form.data['name'], form.files['file'])

    @csrf_protect_m
    def delete_selected(self, request):
        if request.POST.get('post') == 'yes':
            for path in request.POST.getlist('_selected_action'):
                self.model.storage.delete(path)
            return redirect(request.path)
        return render(request, 'pony_admin/storage/delete_selected_confirmation.html', {
            'perms_lacking': False,
            'deletable_objects': request.POST.getlist('_selected_action'),
            'cl': ChangeList(request, self.model, self),
            'action_checkbox_name': '_selected_action',
        })
    delete_selected.short_description = _("Delete selected files")

    def _get_urls(self):
        from django.conf.urls import url
        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^add/$', self._wrap_view(self.add_view), name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self._wrap_view(self.delete_view), name='%s_%s_delete' % info),
        ]
        return urlpatterns
