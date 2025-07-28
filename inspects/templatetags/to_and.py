from django import template

register = template.Library()

@register.filter(name='to_and')
def to_and(value):
    return value.replace(".","a")