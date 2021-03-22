from django import template

register = template.Library()


@register.filter
def percentage_filter(value):
    """
    Converts a decimal to a percentage with a single decimal place.
    """
    try:
        return f"{'%.1f' % (float(value) * 100)}%"
    except Exception:
        print(f'exception: {value}')
        return value
