from django import template
from publish.config.formatting import _format_authors

register = template.Library()
 
@register.filter("format_authors", format_authors)
def format_authors(value):
    return _format_authors(value)
