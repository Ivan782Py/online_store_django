from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.models import User

from app_users.forms import RegistrationForm
from app_users.models import Profile


class RegistrationView(FormView):
    """ Регистрация пользователя """
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = '/'

    def form_valid(self, form):
        """ Создание пользователя """
        fio = form.cleaned_data.get('fio')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password')
        username = email.partition('@')[0]

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        instance = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=instance)

        Profile.objects.create(user=user, phone=phone, fio=fio)

        return super().form_valid(form)
