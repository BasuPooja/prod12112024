from django import template

register = template.Library()

@register.filter(name='convertoInt')
def convertoInt(value):
    return int(value)