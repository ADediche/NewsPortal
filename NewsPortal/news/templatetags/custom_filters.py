from django import template

register = template.Library()

@register.filter()
def censor(value):
    if isinstance(value, str):
        if value.find('избил'):
            return value.replace('избил', 'и....')
        elif value.find('редиска'):
            return value.replace('редиска', 'р....')
    else:
        return 'фильтр ensor не может быть применим к данному объекту'