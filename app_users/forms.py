from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField


class RegistrationForm(forms.Form):
    """ Форма для регистрации пользователя """
    fio = forms.CharField(max_length=50, label=False, widget=forms.TextInput(attrs={'placeholder': 'Ф.И.О'}))
    email = forms.EmailField(label=False, widget=forms.TextInput(attrs={'placeholder': 'email'}))
    phone = PhoneNumberField(label=False, widget=forms.TextInput(attrs={'placeholder': '+7'}))
    password = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Пароль'}))
    password_rep = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Повторите пароль'}))

    def clean(self):
        """ Проверка повторного ввода пароля """
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_rep'):
            raise ValidationError(_('Пароли не совпадают'))

