from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def my_media(value):
    if value:
        return f'{settings.MEDIA_URL}{value}'
    return '/static/img/aboutblank.jpg'
