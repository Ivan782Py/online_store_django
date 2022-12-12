from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaulttags import url

from phonenumber_field.modelfields import PhoneNumberField
from app_shop.models import Product


def get_user_dir(instance, filename):
    return f"users/user_{instance.user.id}"


class Profile(models.Model):
    """ Модель для добавления доп. данных о пользователе в БД """
    USER_STATUS = [
        ('starting', 'стартовый'),
        ('advanced', 'продвинутый'),
        ('best', 'наивысший'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True, verbose_name='телефон')
    status = models.CharField(max_length=10, choices=USER_STATUS, blank=True, default='starting', verbose_name='статус')
    avatar = models.ImageField(upload_to=get_user_dir, blank=True, verbose_name='аватар')
    fio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ф.И.О.')

    class Meta:
        db_table = 'profile'
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self) -> url:
        """ Абсолютный путь к объекту Profile """
        return reverse('user', kwargs={'pk': self.user.id})


class Review(models.Model):
    """ Модель для хранения отзывов о товаре (Product) в БД """
    text = models.TextField(max_length=1000, verbose_name='текст')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now=True, verbose_name='дата создания / изменения')
