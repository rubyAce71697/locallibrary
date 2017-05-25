from django import template
from datetime import datetime


register = template.Library()

@register.filter(name='addClass')
def  addClass(value,arg):
    return value.as_widget(attrs={arg.split(',')[0].strip():arg.split(',')[1].strip()})


@register.filter(name='fine')
def fine(value):
    return (datetime.now().date() - value ).days *10
    