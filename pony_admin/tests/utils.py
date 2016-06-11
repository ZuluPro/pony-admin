from pony_admin.admin import BaseAdmin
from pony_admin.models import Model


class IntModel(Model):
    class Meta:
        app_label = 'pony_admin'
        model_name = 'int'
        verbose_name_plural = 'ints'


class IntsAdmin(BaseAdmin):
    list_display = ['as_float_from_admin', 'as_float_described']

    def get_objects(self, request):
        return [1, 2, 3]

    def as_float_from_admin(self, obj):
        return float(obj)

    def as_float_described(self, obj):
        return float(obj)
    as_float_described.short_description = 'Description'
