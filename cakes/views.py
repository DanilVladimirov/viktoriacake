import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from cakes.models import (Biscuit,
                          Cream,
                          Filling,
                          Decoration,
                          Cake,
                          CakeDiameters,
                          Orders)


def start_page(request):
    return redirect('cakes')


def add_cake(request):
    return render(request, 'add-cake.html')


def view_cakes(request):
    cakes = Cake.objects.exclude(name='Handmade')
    context = {'cakes': cakes}
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    if request.POST and action == 'add_cart':
        cakes_cart = cart.get('cakes')
        curr_cake = request.POST.get('cake_id')
        if cakes_cart is None:
            cake = [{'id': Cake.objects.get(id=curr_cake).id}]
            request.session['cart'] = cart
            cart['cakes'] = cake
            request.session.modified = True
        else:
            cakes_cart.append({'id': Cake.objects.get(id=curr_cake).id})
            cart['cakes'] = cakes_cart
            request.session.modified = True
    return render(request, 'cakes.html', context)


def create_cake(request):
    biscuits = Biscuit.objects.all()
    creams = Cream.objects.all()
    fillings = Filling.objects.all()
    decors = Decoration.objects.all()
    diameters = CakeDiameters.objects.all()
    cart = request.session.get('cart', {})
    action = request.POST.get('action')
    context = {}

    if request.POST:
        bisc = Biscuit.objects.get(id=request.POST.get('biscuit'))
        cream = Cream.objects.get(id=request.POST.get('cream'))
        fill = Filling.objects.get(id=request.POST.get('filling'))
        decor = Decoration.objects.get(id=request.POST.get('decor'))
        diameter = CakeDiameters.objects.get(id=request.POST.get('diameter'))
        cost = (bisc.cost + cream.cost + fill.cost + decor.cost) * diameter.coefficient
        weight = bisc.weight + cream.weight + fill.weight
        handmade = cart.get('handmade')
        handmade_values = {'bisc': bisc.id, 'cream': cream.id,
                           'filling': fill.id, 'decor': decor.id,
                           'cost': cost, 'weight': weight, 'diameter': diameter.id}
        if handmade is None:
            cart = request.session.get('cart', {})
            handmade = [handmade_values]
            request.session['cart'] = cart
            cart['handmade'] = handmade
            request.session.modified = True
        else:
            handmade.append(handmade_values)
            cart['handmade'] = handmade
            request.session.modified = True
    context.update({'biscuits': biscuits,
                    'creams': creams,
                    'fillings': fillings,
                    'decors': decors,
                    'diameters': diameters})
    return render(request, 'create_cake.html', context)


def remover_session(request):
    request.session.clear()
    return HttpResponse('ahaha')


def cart_page(request):
    cart = request.session.get('cart', {})
    action = request.POST.get('action')
    context = {'cakes': [], 'handmade': []}
    if request.POST and action == 'remove':
        cid = int(request.POST.get('cake_id'))
        for el in cart['cakes']:
            if el['id'] == cid:
                index = cart['cakes'].index(el)
                del cart['cakes'][index]
        request.session['cart'] = cart
        request.session.modified = True
    if request.POST and action == 'remove_hcake':
        del cart['handmade'][int(request.POST.get('hcake_id'))]
        request.session['cart'] = cart
        request.session.modified = True
    for el in cart:
        if el == 'handmade':
            for hcake in cart[el]:
                context['handmade'].append({'bisc': Biscuit.objects.get(id=hcake.get('bisc')),
                                            'cream': Cream.objects.get(id=hcake.get('cream')),
                                            'filling': Filling.objects.get(id=hcake.get('filling')),
                                            'decor': Decoration.objects.get(id=hcake.get('decor')),
                                            'cost': hcake.get('cost'),
                                            'weight': hcake.get('weight')})
        elif el == 'cakes':
            for cake in cart[el]:
                context['cakes'].append(Cake.objects.get(id=cake.get('id')))
    return render(request, 'cart-page.html', context)


def cake_details(request, cid):
    cake = Cake.objects.get(id=cid)
    context = {'cake': cake}
    return render(request, 'cake-details.html', context)


def buy_page(request):
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    if request.POST and action == 'create_order':
        list_cakes = []
        for el in cart:
            if el == 'handmade':
                for hcake in cart[el]:
                    new_cake = Cake.objects.create(biscuit_id=Biscuit.objects.get(id=hcake.get('bisc')).id,
                                                   cream_id=Cream.objects.get(id=hcake.get('cream')).id,
                                                   filling_id=Filling.objects.get(id=hcake.get('filling')).id,
                                                   decoration_id=Decoration.objects.get(id=hcake.get('decor')).id,
                                                   diameter_id=CakeDiameters.objects.get(id=hcake.get('diameter')).id,
                                                   cost=float(hcake.get('cost')),
                                                   weight=float(hcake.get('weight')),
                                                   name='Кастомний')
                    new_cake.save()
                    list_cakes.append(new_cake)
            elif el == 'cakes':
                for cake in cart[el]:
                    list_cakes.append(Cake.objects.get(id=cake.get('id')))
        new_order = Orders.objects.create(
                                          name=request.POST.get('name'),
                                          surname=request.POST.get('surname'),
                                          telephone=request.POST.get('telephone'),
                                          address=request.POST.get('address'),
                                          comment=request.POST.get('comment'))
        new_order.cakes.set(list_cakes)
        new_order.save()
    return render(request, 'buy-page.html')


def orders_page(request):
    context = {}
    context.update({'orders': Orders.objects.all()})
    action = request.POST.get('action')
    if request.POST and action == 'ready':
        order_id = request.POST.get('order_id')
        order = Orders.objects.get(id=int(order_id))
        for cake in order.cakes.all():
            if cake.name == 'Кастомний':
                cake.delete()
        order.delete()
    return render(request, 'orders-page.html', context)


def addcart(request):
    data_response = {}
    cart = request.session.get('cart', {})
    if request.POST:
        cakes_cart = cart.get('cakes')
        curr_cake = request.POST.get('cakeid')
        if cakes_cart is None:
            cake = [{'id': Cake.objects.get(id=curr_cake).id}]
            request.session['cart'] = cart
            cart['cakes'] = cake
            request.session.modified = True
        else:
            have_cake = False
            for cake in cakes_cart:
                if int(cake['id']) == int(curr_cake):
                    have_cake = True
            if not have_cake:
                cakes_cart.append({'id': Cake.objects.get(id=curr_cake).id})
                cart['cakes'] = cakes_cart
                request.session.modified = True
        data_response.update({'success': True})
    return HttpResponse(json.dumps(data_response), content_type='application/json')
