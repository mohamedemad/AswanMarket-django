from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponse
from carts.models import Carts, CartItem
from store.models import Product


# Create your views here.


def _cart_id(request):
    carts = request.session.session_key
    if not carts:
        carts = request.session.create()
    return carts


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        carts = Carts.objects.get(cart_id=_cart_id(request))
    except Carts.DoesNotExist:
        carts = Carts.objects.create(cart_id=_cart_id(request))
    carts.save()
    try:
        cart_item = CartItem.objects.get(product=product, carts=carts)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, carts=carts)
        cart_item.save()

    return redirect('cart')


# decrement minus button
def remove_cart(request, product_id):
    cart = Carts.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, carts=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Carts.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, carts=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        carts = Carts.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(carts=carts, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    return render(request, 'store/carts.html',
                  context={'total': total, 'quantity': quantity, 'cart_items': cart_items, 'tax': tax,
                           'grand_total': grand_total})
