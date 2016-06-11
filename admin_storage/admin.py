from django.contrib import admin
from django.http import HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.options import csrf_protect_m
from django.shortcuts import render
from django.utils.safestring import mark_safe


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
        else:
            value = None
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
