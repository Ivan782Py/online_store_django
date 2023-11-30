from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(BaseUserCreationForm):
    """ Форма регистрации пользователя """

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {'username': forms.EmailInput()}
        labels = {
            'username': 'Email',
            'password1': 'Пароль',
            'password2': 'Повторите пароль'
        }
