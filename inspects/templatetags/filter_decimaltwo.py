from django import template

register = template.Library()
@register.filter(name='filter_decimaltwo')
def filter_decimaltwo(value):
    # print("hellooooooooooo",value)
    a="{:.2f}".format(float(value))
    return a