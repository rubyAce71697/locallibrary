from django import template


register = template.Library()

@register.filter(name='addClass')
def  addClass(value,arg):
    return value.as_widget(attrs={arg.split(',')[0].strip():arg.split(',')[1].strip()})

