from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app_user.views import RegistrationView, ProfileView, LoginUserView, LogoutUserView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
