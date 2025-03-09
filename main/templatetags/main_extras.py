from django import template
from django.template.defaultfilters import dictsort

register = template.Library()

@register.filter
def groupby(value, arg):
    """
    Group items into lists of size 'arg'.
    Example: items|groupby:2
    """
    try:
        arg = int(arg)
    except (ValueError, TypeError):
        return [value]
    
    result = []
    temp = []
    
    for item in value:
        if len(temp) < arg:
            temp.append(item)
        if len(temp) == arg:
            result.append(temp)
            temp = []
    
    if temp:
        result.append(temp)
    
    return result
