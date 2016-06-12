from libcloud.compute.providers import get_driver
from django.utils.translation import ugettext_lazy as _
from pony_admin.models import Model


class BaseComputeModel(Model):
    compute = None

    class Meta(object):
        app_label = 'pony_admin'
        abstract = True


class GandiComputeModel(BaseComputeModel):
    compute = get_driver('gandi')('YrBXg9jQ0zNHta4ulNlNvn15')

    class Meta:
        app_label = 'pony_admin'
        model_name = 'gandi_compute'
        verbose_name_plural = _("Gandi VM's")
