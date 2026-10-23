from django import template

register = template.Library()


@register.filter
def day_items(mapping, day):
    return mapping.get(day, {"events": [], "tasks": [], "projects": []})
