from django.contrib import admin
from django.http import HttpResponseBadRequest
from django.db.models.options import Options, DEFAULT_NAMES
from django.core.files.storage import get_storage_class
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.options import csrf_protect_m
from django.shortcuts import render, redirect
from django.utils.six import with_metaclass
from django.contrib.staticfiles.storage import StaticFilesStorage


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


class StorageAdmin(admin.ModelAdmin):
    change_list_template = 'admin_storage/changelist.html'
    change_form_template = 'admin_storage/change_form.html'
    actions = ['delete_selected']

    def has_module_permission(self, request):
        return True

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and request.POST.get('action'):
            action_name = request.POST['action']
            if action_name not in self.actions:
                return HttpResponseBadRequest()
            action = getattr(self, action_name)
            return action(request)

        cl = ChangeList(request, self.model, self)
        path = request.GET.get('path', '')
        storage = self.model.storage
        return render(request, self.change_list_template, {
            'cl': cl,
            'path': path,
            'storage': storage,
            'files': storage.listdir(path),
            'action_form': self.action_form,
            'has_add_permission': True,
        })

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
