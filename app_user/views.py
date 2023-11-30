from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.forms import Form
from django.template.defaulttags import url
from django.urls import reverse
from django.views.generic import FormView, DetailView

from app_user.forms import RegistrationForm
from app_user.models import Profile


class RegistrationView(FormView):
    """ Страница регистрации пользователя """
    form_class = RegistrationForm
    template_name = 'user/registration.html'

    @transaction.atomic
    def form_valid(self, form) -> Form:
        """ Регистрация пользователя """
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        instance = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=instance)

        Profile.objects.create(user=user)

        return super().form_valid(form)

    def get_success_url(self) -> url:
        return reverse('profile')


class LoginUserView(LoginView):
    """ Аутентификация пользователя """
    template_name = 'user/login.html'

    def get_success_url(self) -> url:
        return self.request.GET.get('next', '/')


class LogoutUserView(LogoutView):
    """ Выход из учетной записи """
    next_page = '/'


class ProfileView(LoginRequiredMixin, DetailView):
    """ Страница профиля пользователя """
    template_name = 'user/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None) -> object:
        obj = Profile.objects.get(user=self.request.user)
        return obj
