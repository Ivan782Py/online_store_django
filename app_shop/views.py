from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.db.models import Sum, Min

from app_shop.models import Product, Category


class HomeView(View):
    """ Главная страница """

    def get(self, request: HttpRequest) -> HttpResponse:
        """ Получение данных с сервера """
        top_categories = Category.objects.select_related('parent').prefetch_related('products').filter(
            favorites=True).annotate(min_price=Min('products__price')).order_by('-super_category')[:3]

        product = Product.objects.select_related('category').prefetch_related('purchases')
        top_products = product.filter(purchases__isnull=False).annotate(
            num_of_purchased=Sum('purchases__quantity_of_product')).order_by('-num_of_purchased')[:8]
        limited_ed = product.filter(status='limited').order_by('count')[:16]

        context = {
            'top_categories': top_categories,
            'top_products': top_products,
            'limited_ed': limited_ed,
        }

        return render(request, 'index.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """ Запрос к серверу с параметрами фильтра из поля поиска """
        pass
