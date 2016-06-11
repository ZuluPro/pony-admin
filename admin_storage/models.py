from django.db.models.options import Options


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
