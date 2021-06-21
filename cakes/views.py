import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from cakes.forms import UserRegisterForm
from cakes.models import (Biscuit,
                          Cream,
                          Filling,
                          Decoration,
                          Cake,
                          CakeDiameters,
                          Orders,
                          WishList,
                          Recommended,
                          Info)


def start_page(request):
    return redirect('cakes')


def view_cakes(request):
    cakes = Cake.objects.exclude(name='Кастомний')
    context = {'cakes': cakes}
    return render(request, 'cakes.html', context)


def create_cake(request):
    biscuits = Biscuit.objects.all()
    creams = Cream.objects.all()
    fillings = Filling.objects.all()
    decors = Decoration.objects.all()
    diameters = CakeDiameters.objects.all()
    recommended = Recommended.objects.all()[:2]
    cart = request.session.get('cart', {})
    action = request.POST.get('action')
    context = {}
    context.update({'recommended': recommended})
    if request.POST:
        try:
            bisc = Biscuit.objects.get(id=request.POST.get('biscuit'))
            cream = Cream.objects.get(id=request.POST.get('cream'))
            fill = Filling.objects.get(id=request.POST.get('filling'))
            decor = Decoration.objects.get(id=request.POST.get('decor'))
            diameter = CakeDiameters.objects.get(id=request.POST.get('diameter'))
        except:
            context.update({'biscuits': biscuits,
                            'creams': creams,
                            'fillings': fillings,
                            'decors': decors,
                            'diameters': diameters,
                            'bad': True})
            return render(request, 'create_cake.html', context)
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
        context.update({'good': True})
    context.update({'biscuits': biscuits,
                    'creams': creams,
                    'fillings': fillings,
                    'decors': decors,
                    'diameters': diameters})
    return render(request, 'create_cake.html', context)


def cart_page(request):
    cart = request.session.get('cart', {})
    action = request.POST.get('action')
    context = {'cakes': [], 'handmade': []}
    total_cost = 0
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
                total_cost += hcake.get('cost')
        elif el == 'cakes':
            for cake in cart[el]:
                context['cakes'].append(Cake.objects.get(id=cake.get('id')))
                total_cost += Cake.objects.get(id=cake.get('id')).price()

    context.update({'total_cost': total_cost})
    print(context)
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
        request.session['cart'] = {}
        request.session.modified = True
        return render(request, 'buy-page.html', {'ordered': True})
    if len(cart) == 0:
        return redirect('start_page')
    return render(request, 'buy-page.html')


@login_required
def admin_page(request):
    if not request.user.is_superuser:
        return redirect('start_page')
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


@login_required
def add_to_wishlist(request):
    if request.POST:
        if request.user.is_authenticated:
            user = request.user
            cake = Cake.objects.get(id=request.POST.get('cakeid'))
            wish_list = WishList.objects.get_or_create(user=user)[0]
            wish_list.cakes.add(cake)
            data_response = {'success': True}
            return HttpResponse(json.dumps(data_response), content_type='application/json')
        else:
            return redirect('create_cake')


@login_required
def del_from_wishlist(request):
    if request.POST:
        user = request.user
        cake = Cake.objects.get(id=request.POST.get('cakeid'))
        wish_list = WishList.objects.get_or_create(user=user)[0]
        wish_list.cakes.remove(cake)
        data_response = {'success': True}
        return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required(login_url='login_page')
def profile_page(request):
    if request.user.is_superuser:
        return redirect('orders_page')
    context = {}
    action = request.POST.get('action')
    if request.POST and action == "change":
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.info.phone = request.POST.get('phone')
        user.info.address = request.POST.get('address')
        user.save()
    wishlist = WishList.objects.get(user=request.user)
    context.update({'wishlist': wishlist})
    return render(request, 'profile-page.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    else:
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('start_page')
    return render(request, 'login-page.html')


def logout_page(request):
    logout(request)
    return redirect('login_page')


def registration_page(request):
    context = {}
    if request.POST:
        form = UserRegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            new_user = form.save()
            new_info = Info.objects.create(user=new_user,
                                           phone=request.POST.get('phone'),
                                           address=request.POST.get('address'))
            new_info.save()
            new_wishlist = WishList.objects.create(user=new_user)
            new_wishlist.save()
            return redirect('login_page')
    return render(request, 'register-page.html', context)


def test(request):

    return HttpResponse(json.dumps({'haahah': True}), content_type='application/json')