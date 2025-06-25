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
        return 'фильтр censor не может быть применим к данному объекту'

@register.filter()
def address(value, index):
    address = "../subscrib/" + str(index)
    return address
