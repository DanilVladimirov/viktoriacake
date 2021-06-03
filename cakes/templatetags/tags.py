from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(request, cid):
    have_cake = False
    cart = request.session.get('cart', {})
    cakes_cart = cart.get('cakes')
    for cake in cakes_cart:
        if int(cake['id']) == int(cid):
            have_cake = True
    return have_cake
