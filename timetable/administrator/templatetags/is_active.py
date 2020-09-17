# Inside custom tag - is_active.py
from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag
def is_active(request, url):
    if request.path in reverse(url):
        return "active"
    return ""
