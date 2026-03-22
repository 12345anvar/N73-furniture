from django import template

register = template.Library()


@register.simple_tag
def get_full_path(path, code):
    split_path = path.split('/')
    split_path[1] = code
    return '/'.join(split_path)


@register.filter
def in_cart(product, request):
    cart = request.session.get('cart', [])
    return product.id in cart