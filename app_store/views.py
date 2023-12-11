from django.db.models import Sum, QuerySet, Max, Min
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from app_store.models import Product, Category


class HomePageView(TemplateView):
    """ Главная страница """
    template_name = 'store/index.html'

    def get_context_data(self, **kwargs) -> dict:
        """ Передаем в контекст объекты из БД, выбранные по условиям. """
        products = Product.objects.select_related('category').prefetch_related('purchases').exclude(status='default')

        top_product_list = products.filter(status='top').annotate(
            num_of_purchases=Sum('purchases__quantity_of_product')).order_by('-num_of_purchases')[:8]
        limited_product_list = products.filter(status='limit_ed')[:16]
        favorites_category_list = Category.objects.select_related('parent').filter(
            favorites__isnull=False).order_by('-changed_in')[:3]

        context = super().get_context_data(**kwargs)

        context['top_product_list'] = top_product_list
        context['limited_product_list'] = limited_product_list
        context['favorites_category_list'] = favorites_category_list

        return context


class CatalogPageView(ListView):
    """ Страница каталога товаров """
    model = Product
    template_name = 'store/catalog.html'

    # paginate_by = 2

    def get_queryset(self) -> QuerySet[object]:
        """ Получаем список товаров по условиям фильтрации """
        queryset = self.model.objects.select_related('category').prefetch_related('purchases')

        slug = self.kwargs['slug']
        search = self.request.GET.get('search')
        status_list = self.request.GET.getlist('status-list')
        min_price = self.request.GET.get('min-price')
        max_price = self.request.GET.get('max-price')

        if slug and not slug == 'all':
            queryset = queryset.filter(category__slug=slug)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if min_price:
            queryset = queryset.filter(price__range=(min_price, max_price))
        if status_list:
            queryset = queryset.filter(status__in=status_list)

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        """ Передаем дополнительные параметры в контекст """
        context = super().get_context_data(**kwargs)
        prices = self.get_queryset().aggregate(Max('price'), Min('price'))

        context['get_slug'] = self.kwargs['slug']
        context['product_status_list'] = Product.PRODUCT_STATUS
        try:
            context['max_price'] = int(prices['price__max'])
            context['min_price'] = int(prices['price__min'])
        except TypeError as er:
            context['not_value'] = er

        return context


class ProductDetailView(DetailView):
    """ Страница с детальной инфо о товаре """
    model = Product
    template_name = 'store/product_detail.html'


class AboutView(TemplateView):
    """ Описание магазина """
    template_name = 'store/about.html'
