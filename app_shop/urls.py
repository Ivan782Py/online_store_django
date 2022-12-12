from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app_shop.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
