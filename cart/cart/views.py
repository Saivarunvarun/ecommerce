from ecommerceapp.models import Product
from django.shortcuts import render, redirect
from .models import Cart, Cart_items
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id_(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id_(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id_(request))
        cart.save()
    try:
        cart_item = Cart_items.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except Cart_items.DoesNotExist:
        cart_item = Cart_items.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id_(request))
        cart_items = Cart_items.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))
