from django.db import models
from django.contrib.auth.models import User
from django.template.defaulttags import url
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

from app_store.models import Product


def get_user_dir(instance, filename) -> str:
    """ Путь загрузки и записи аватарки пользователя """
    return f"users/user_{instance.user.id}"


class Profile(models.Model):
    """ Профиль пользователя """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(unique=True)
    fio = models.CharField(max_length=50, blank=True, verbose_name='Ф.И.О.')
    avatar = models.ImageField(upload_to=get_user_dir, blank=True, verbose_name='аватар')
    city = models.CharField(max_length=30, blank=True, verbose_name='город')
    address = models.CharField(max_length=200, blank=True, verbose_name='адрес')
    created_at = models.DateField(auto_now_add=True, verbose_name='создан')

    class Meta:
        db_table = 'profiles'
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self) -> str:
        """ Получаем имя пользователя """
        return self.fio.split()[1]

    def get_absolute_url(self) -> url:
        """ Абсолютный путь к профилю пользователя """
        return reverse('user', kwargs={'pk': self.user_id})


class Review(models.Model):
    """ Модель отзыва о товаре """
    text = models.TextField(max_length=1000, verbose_name='текст')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now=True, verbose_name='дата создания / изменения')
