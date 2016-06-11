import os
from django.template import Library


register = Library()


@register.filter
def parent_dir(path, *args):
    return os.path.split(path)[0]
