# In your Django app, create a templatetags directory if not already exists.
# Inside templatetags directory, create a Python file, e.g., custom_filters.py

# custom_filters.py

from django import template

register = template.Library()

@register.filter
def num_range(value):
    return range(value)
