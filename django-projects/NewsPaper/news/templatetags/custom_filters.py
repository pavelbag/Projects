from django import template


register = template.Library()


@register.filter()
def censor(value):
    # Вызываем исключение если значение не строка
    if type(value) != str:
        raise TypeError("Неверный тип данных")

    value = f'{value}'
    value = value.replace("Редиска", "Р...")
    value = value.replace("Кабачок", "К...")

    return value