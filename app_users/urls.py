from django.urls import path

from app_users.views import RegistrationView

urlpatterns = [
    path('registr/', RegistrationView.as_view(), name='registration')
]
