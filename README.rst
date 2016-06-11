Pony Admin
==========

Pony Admin helps you to add any objects in Django Admin interface. Get what
you want sorted with models, media, static or files from any storage, data
from cache or whatever.

Install
-------

Just: ::
    pip install pony-admin

And add ``'admin_storage'`` in your ``settings.INSTALLED_APPS``


How to deal with
----------------

Create a ``Model`` class for set common data of your datastore, example: ::

    from admin_storage.models import Model

    class IntModel(Model):
        class Meta:
            app_label = 'admin_storage'
            model_name = 'int'
            verbose_name_plural = 'ints'

Create a ``ModelAdmin`` class for set admin options: ::

    from admin_storage.admin import BaseAdmin

    class IntsAdmin(BaseAdmin):
        list_display = ['as_float_from_admin', 'as_float_described']

        def get_objects(self, request):
            return [1, 2, 3]

        def as_float_from_admin(self, obj):
            return float(obj)

        def as_float_described(self, obj):
            return float(obj)
        as_float_described.short_description = 'Description'


And register them, in a module launched at Django's startup: ::

    from django.contrib import admin

    admin.site.register([IntModel], IntsAdmin)

It's batteries included
-----------------------

Because most of you don't want to lost time for make someting operational,
below a listing of key-in-hand admin modules. You'll just have to register
for use them.

Media storage
~~~~~~~~~~~~~

Allow to navigate in directories, delete and add files. ::

    from django.contrib import admin
    from admin_storage.storage.models import MediaStorageModel
    from admin_storage.storage.admin import StorageAdmin

    admin.site.register([MediaStorageModel], StorageAdmin)

Static storage
~~~~~~~~~~~~~~

Same as Media storage but for static files. ::

    from django.contrib import admin
    from admin_storage.storage.models import StaticStorageModel
    from admin_storage.storage.admin import StorageAdmin

    admin.site.register([StaticStorageModel], StorageAdmin)

Any storage
~~~~~~~~~~~

You can have any storage simply, just create a ``Model`` for it, for example:

::

    from admin_storage.storage.models import BaseStorageModel

    class MediaStorageModel(BaseStorageModel):
        storage = MyStorage()

        class Meta:
            app_label = 'admin_storage'
            model_name = 'my_storage'
            verbose_name_plural = 'my files'
