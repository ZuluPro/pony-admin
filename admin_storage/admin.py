import os
from django.contrib import admin
from django.http import HttpResponseBadRequest
from django.db.models.options import Options
from django.core.files.storage import get_storage_class
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.options import csrf_protect_m
from django.shortcuts import render, redirect
from django.utils.six import with_metaclass
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils.safestring import mark_safe


media_storage = get_storage_class()()
static_storage = StaticFilesStorage()


class ChangeList(object):
    def __init__(self, request, model, modeladmin):
        self.request = request
        self.model = model
        self.model_admin = modeladmin
        self.opts = model._meta
        self.result_count = 0
        self.full_result_count = 0
        self.date_hierarchy = None
        self.list_display = ('name')

    def get_ordering_field_columns(self):
        return []


class BaseAdmin(admin.ModelAdmin):
    list_display = []
    change_list_template = 'admin_storage/changelist.html'
    change_form_template = 'admin_storage/change_form.html'

    def get_objects(self, request):
        raise NotImplementedError('')

    def has_module_permission(self, request):
        return True

    @staticmethod
    def check(model):
        return []

    def _get_field_value(self, field_name, instance):
        for obj in (self, self.model, instance):
            if hasattr(obj, field_name):
                value = getattr(obj, field_name)
                break
            elif isinstance(obj, dict) and field_name in obj:
                value = obj[field_name]
                break
        if hasattr(value, '__call__'):
            try:
                value = value()
            except TypeError:
                value = value(instance)
        if getattr(value, 'allow_tags', False):
            value = mark_safe(value)
        return value

    def _get_field_name(self, field_name):
        for obj in (self, self.model):
            if hasattr(obj, field_name):
                value = getattr(obj, field_name)
                break
            elif isinstance(obj, dict) and field_name in obj:
                value = obj[field_name]
                break
        if hasattr(value, 'short_description'):
            return value.short_description
        return field_name

    def get_results(self, request):
        results = {'names': [], 'rows': []}
        results['names'] = [self._get_field_name(name)
                            for name in self.list_display]
        objects = self.get_objects(request)
        for obj in objects:
            values = [obj]
            for field in self.list_display:
                values.append(self._get_field_value(field, obj))
            results['rows'].append(values)
        return results

    def _get_changelist_context(self, request):
        return {}

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and request.POST.get('action'):
            action_name = request.POST['action']
            if action_name not in self.actions:
                return HttpResponseBadRequest()
            action = getattr(self, action_name)
            return action(request)

        cl = ChangeList(request, self.model, self)
        context = self._get_changelist_context(request)
        context.update({
            'cl': cl,
            'results': self.get_results(request),
            'action_form': self.action_form,
            'has_add_permission': True,
        })
        return render(request, self.change_list_template, context)


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


class ModelBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__

        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        # Get meta from parent class
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        app_label = getattr(attr_meta, 'app_label', None)
        # Get meta from created child
        new_meta = getattr(new_class, 'Meta', None)
        abstract = abstract or getattr(new_meta, 'abstract', False)
        app_label = app_label or getattr(new_meta, 'app_label', None)

        # Create _meta attribute
        new_class._meta = Options(new_meta, app_label=app_label)
        for attr_name, attr in attr_meta.__dict__.items():
            if attr_name.startswith('_'):
                continue
            setattr(new_class._meta, attr_name, attr)
        # Put class attrs
        for attr_name, attr in attrs.items():
            setattr(new_class, attr_name, attr)
        return new_class

    def get_field(self, field):
        return ''

    def get_ordered_objects(self):
        return False

    def get_change_permission(self):
        return 'change_%s' % self.model_name


class BaseStorageModel(with_metaclass(ModelBase)):
    storage = None

    class Meta(object):
        app_label = 'admin_storage'
        abstract = False


class MediaStorageModel(BaseStorageModel):
    storage = media_storage

    class Meta:
        app_label = 'admin_storage'
        model_name = 'media'
        verbose_name_plural = _('media files')


class StaticStorageModel(BaseStorageModel):
    storage = static_storage

    class Meta:
        app_label = 'admin_storage'
        model_name = 'static'
        verbose_name_plural = _('static files')


admin.site.register([MediaStorageModel, StaticStorageModel], StorageAdmin)
# admin.site.register([FakeModel(Foo)], StorageAdmin)
