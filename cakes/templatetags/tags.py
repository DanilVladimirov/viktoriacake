from django import template
from cakes.models import WishList, Cake

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(request, cid):
    have_cake = False
    cart = request.session.get('cart', {})
    cakes_cart = cart.get('cakes')
    if cakes_cart is not None:
        for cake in cakes_cart:
            if int(cake['id']) == int(cid):
                have_cake = True
    return have_cake


@register.filter(name='is_in_wishlist')
def is_in_wishlist(request, cid):
    if request.user.is_authenticated:
        wishlist = WishList.objects.filter(user=request.user)
        if wishlist.exists():
            wishlist = WishList.objects.get(user=request.user)
            cake = Cake.objects.get(id=cid)
            if cake in wishlist.cakes.all():
                return True
            else:
                return False
