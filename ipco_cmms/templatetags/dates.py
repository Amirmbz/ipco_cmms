from django import template
from django.utils import translation
from ipco_cmms.utils import to_jalali

register = template.Library()


@register.filter
def display_date(value):
    if not value:
        return ''
    if translation.get_language() == 'fa':
        return to_jalali(value)
    return value