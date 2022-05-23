from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter()
def find_with_GET(value):
    return mark_safe(f'<a href="https://www.google.com/search?q={value}" target="_blank">{value}</a>')
