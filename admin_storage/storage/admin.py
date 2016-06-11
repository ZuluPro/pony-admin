import os
from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.shortcuts import render, redirect
from admin_storage.admin import BaseAdmin, ChangeList
from admin_storage.storage.models import MediaStorageModel, StaticStorageModel


class StorageAdmin(BaseAdmin):
    list_display = ['get_url_link']
    change_list_template = 'admin_storage/changelist_storage.html'
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
        return {
            'path': request.GET.get('path', ''),
            'storage': self.model.storage,
            'files': self.get_objects(request),
        }

    @csrf_protect_m
    def add_view(self, request):
        if request.method == 'POST':
            file_ = request.FILES['file']
            self.model.storage.save(file_.name, file_)
            # TODO: Clear urls
            return redirect('/admin/admin_storage/storage/')
        return render(request, self.change_form_template, {
        })

    @csrf_protect_m
    def delete_selected(self, request):
        if request.POST.get('post') == 'yes':
            for path in request.POST.getlist('_selected_action'):
                self.model.storage.delete(path)
            return redirect(request.path)
        return render(request, 'admin_storage/delete_selected_confirmation.html', {
            'perms_lacking': False,
            'deletable_objects': request.POST.getlist('_selected_action'),
            'cl': ChangeList(request, self.model, self),
            'action_checkbox_name': '_selected_action',
        })


admin.site.register([MediaStorageModel, StaticStorageModel], StorageAdmin)
