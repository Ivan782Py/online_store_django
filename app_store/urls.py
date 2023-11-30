from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app_store.views import HomePageView, CatalogPageView, ProductDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('catalog/<slug:slug>/?page=<int:page>/', CatalogPageView.as_view(), name='catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
