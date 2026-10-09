from ..models import Post
from django import (
    forms,
    template,
)


register = template.Library()


@register.filter()
def filter_bootstrap_field(value: forms.boundfield.BoundField):
    # Вызываем исключение если не тот тип данных
    if type(value) != forms.boundfield.BoundField:
        raise TypeError("Неверный тип данных")

    if value.widget_type == 'checkbox':
        value.field.widget.attrs['class'] = 'form-check-input'
    if value.widget_type == 'password':
        value.field.widget.attrs['class'] = 'form-control'
    if value.widget_type == 'text':
        value.field.widget.attrs['class'] = 'form-control'

    return value


@register.filter()
def filter_censor(value):
    # Вызываем исключение если значение не строка
    if type(value) != str:
        raise TypeError("Неверный тип данных")

    value = f'{value}'
    value = value.replace("Редиска", "Р...")
    value = value.replace("Кабачок", "К...")

    return value


@register.filter()
def filter_post_categories(value):
    return ','.join(a.name for a in value.all())


@register.filter()
def filter_post_type(value):
    return dict(Post.POST_TYPES).get(value)