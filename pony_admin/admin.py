from functools import update_wrapper

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
    """
    Base admin class for create others Admin class.
    """
    list_display = []
    change_list_template = 'pony_admin/changelist.html'
    change_form_template = 'pony_admin/change_form.html'

    def get_objects(self, request):
        """
        Get objects listed in admin interface.
        """
        raise NotImplementedError('')

    def has_module_permission(self, request):
        return True

    @staticmethod
    def check(model):
        """Dummy check method."""
        return []

    def _get_field_value(self, field_name, instance):
        """
        Get the value for an attribute in ``self.list.display``.

        The attribute is searched in ModelAdmin, Model and after instance.
        It tries to copy the Django Admin behavior.
        """
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
        """
        Get the title for an attribute in ``self.list.display``.

        The attribute is searched in ModelAdmin, Model and after instance.
        It tries to copy the Django Admin behavior.
        """
        for obj in (self, self.model):
            if hasattr(obj, field_name):
                value = getattr(obj, field_name)
                break
            elif isinstance(obj, dict) and field_name in obj:
                value = obj[field_name]
                break
        else:
            return field_name
        if hasattr(value, 'short_description'):
            return value.short_description
        return field_name

    def get_results(self, request):
        """
        Get results sorted for list in admin interfaces.
        """
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

        context = self._get_changelist_context(request)
        context.update({
            'actions': self.get_actions(),
            'results': self.get_results(request),
            'action_form': self.action_form,
            'has_add_permission': True,
            'meta': self.model._meta,
        })
        return render(request, self.change_list_template, context)

    def _wrap_view(self, view):
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view)(*args, **kwargs)
        return update_wrapper(wrapper, view)

    def _get_urls(self):
        """Override this method for add simply urls."""
        return []

    def get_urls(self):
        from django.conf.urls import url

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^$', self._wrap_view(self.changelist_view), name='%s_%s_changelist' % info),
            # url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
            # url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        ] + self._get_urls()
        return urlpatterns

    def get_actions(self):
        return [(name, self._get_field_name(name)) for name in self.actions]
