import os
from django.contrib import admin
from pony_admin.storage.admin import StorageAdmin
from pony_admin.storage.models import MediaStorageModel, StaticStorageModel


if os.environ.get('REGISTER', False):
    admin.site.register([MediaStorageModel, StaticStorageModel], StorageAdmin)
