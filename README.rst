Pony Admin
==========

Pony Admin helps you to add any objects in Django Admin interface. Get what
you want sorted with models, media, static or files from any storage, data
from cache or whatever.

Install
-------

Just: ::
    pip install pony-admin

And add ``'pony_admin'`` in your ``settings.INSTALLED_APPS``


How to deal with
----------------

Create a ``Model`` class for set common data of your datastore, example: ::

    from pony_admin.models import Model

    class IntModel(Model):
        class Meta:
            app_label = 'pony_admin'
            model_name = 'int'
            verbose_name_plural = 'ints'

Create a ``ModelAdmin`` class for set admin options: ::

    from pony_admin.admin import BaseAdmin

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

Allow to navigate in directories, delete and add files. Just add
``'pony_admin.storage'`` in your ``settings.INSTALLED_APPS``::

    from django.contrib import admin
    from pony_admin.storage.models import MediaStorageModel
    from pony_admin.storage.admin import StorageAdmin

    admin.site.register([MediaStorageModel], StorageAdmin)

Static storage
~~~~~~~~~~~~~~

Same as Media storage but for static files. ::

    from django.contrib import admin
    from pony_admin.storage.models import StaticStorageModel
    from pony_admin.storage.admin import StorageAdmin

    admin.site.register([StaticStorageModel], StorageAdmin)

Any storage
~~~~~~~~~~~

You can have any storage simply, just create a ``Model`` for it, for example:

::

    from pony_admin.storage.models import BaseStorageModel

    class MediaStorageModel(BaseStorageModel):
        storage = MyStorage()

        class Meta:
            app_label = 'pony_admin'
            model_name = 'my_storage'
            verbose_name_plural = 'my files'
