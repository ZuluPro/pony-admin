import os
from django.template import Library
from django.shortcuts import render


register = Library()


@register.simple_tag(takes_context=True)
def storage_url(context):
    path = os.path.join(context['path'], context['file'])
    return context['storage'].url(path)


@register.filter
def parent_dir(path, *args):
    return os.path.split(path)[0]
