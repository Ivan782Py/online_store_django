from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from app_store.models import Product

from app_cart.cart import Cart


@require_POST
def cart_add(request, product_id):
    """ Добавление товара или увеличение количества """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_POST
def cart_reduce(request, product_id):
    """ Уменьшение кол-ва товара на 1 """
    cart = Cart(request)
    cart.reduce(product_id=product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, product_id):
    """ Удаление позиции из корзины """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_detail(request):
    """ Корзина товаров """
    return render(request, 'cart/cart_detail.html')
