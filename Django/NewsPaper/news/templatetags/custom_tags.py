from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    result = context['request'].GET.copy()

    for key, value in kwargs.items():
        result[key] = value

    return result.urlencode()