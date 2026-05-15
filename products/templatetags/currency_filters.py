from django import template

register = template.Library()

@register.filter
def currency_vnd(value):
    try:
        value = int(float(value))
        return f"{value:,}".replace(",", ".") + "đ"
    except (ValueError, TypeError):
        return value

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except:
        return 0

