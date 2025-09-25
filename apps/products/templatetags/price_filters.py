from django import template

register = template.Library()

@register.filter
def price(value):
    """
    نمایش عدد با جداکننده سه‌رقمی + کلمه 'تومان'
    """
    if value is None:
        return ""
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".") + " تومان"
    except (ValueError, TypeError):
        return value
