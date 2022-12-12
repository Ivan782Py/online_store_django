from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView

from app_shop.models import Product, Category


class MainView(View):
    """ Главная страница """

    def get(self, request: HttpRequest) -> HttpResponse:
        categories = Category.objects.select_related('parent').filter(parent__isnull=True).order_by('-super_category')
        top_categories = categories.filter(favorites=True)[:3]
        products = Product.objects.select_related('category').all()
        return render(request, 'index.html', context={'categories': categories, 'top_categories': top_categories,
                                                      'products': products})
