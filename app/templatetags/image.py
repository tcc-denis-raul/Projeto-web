from django import template
import os
register = template.Library()

@register.filter(name="exist_path")
def exist_path(value):
    return os.path.exists('{}/app/static/{}'.format(os.getcwd(), value))

