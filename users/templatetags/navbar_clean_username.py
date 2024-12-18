from django import template

register = template.Library()


@register.filter(name="clean_username")
def clean_username(value):
    return value.split("@")[0]
