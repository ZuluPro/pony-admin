from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import get_storage_class
from django.contrib.staticfiles.storage import StaticFilesStorage
from pony_admin.models import Model


class BaseStorageModel(Model):
    storage = None

    class Meta(object):
        app_label = 'pony_admin'
        abstract = True


class MediaStorageModel(BaseStorageModel):
    storage = get_storage_class()()

    class Meta:
        app_label = 'pony_admin'
        model_name = 'media'
        verbose_name = _('media file')
        verbose_name_plural = _('media files')


class StaticStorageModel(BaseStorageModel):
    storage = StaticFilesStorage()

    class Meta:
        app_label = 'pony_admin'
        model_name = 'static'
        verbose_name = _('static file')
        verbose_name_plural = _('static files')
