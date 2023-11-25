from django.contrib.auth.models import User
from django.db import models
from django.template.defaulttags import url
from django.urls import reverse


class Product(models.Model):
    """ Модель товара """
    PRODUCT_STATUS = [
        ('top', 'топ продаж'),
        ('limit_ed', 'ограниченное издание'),
        ('default', 'простой')
    ]
    name = models.CharField(max_length=30, verbose_name='название')
    count = models.PositiveIntegerField(default=0, verbose_name='количество')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='цена')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='категория')
    status = models.CharField(max_length=10, choices=PRODUCT_STATUS, default='default', verbose_name='статус')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='изображение')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата первого поступления')
    description = models.TextField(max_length=5000, verbose_name='описание')

    class Meta:
        db_table = 'products'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> str:
        """ Строковое представление объекта product """
        return self.name

    def get_absolute_url(self) -> url:
        """ Получить абсолютный путь к объекту product по id """
        return reverse('product', kwargs={'pk': self.id})

    def get_short_description(self) -> str:
        """ Сократить длинное описание """
        if len(self.description) > 50:
            return self.description[:48] + '...'
        return self.description


class Category(models.Model):
    """ Модель категории """
    name = models.CharField(max_length=15, verbose_name='название')
    slug = models.SlugField(max_length=10, verbose_name='url')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name='родительская категория')
    favorites = models.BooleanField(default=False, verbose_name='избранное')
    icon = models.FileField(upload_to='categories/', blank=True, null=True, help_text='.svg', verbose_name='иконка')
    changed_in = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    class Meta:
        db_table = 'categories'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        """ Строковое представление объекта category """
        return self.name

    def get_absolute_url(self) -> url:
        """ Получить абсолютный путь к объекту category по слагу """
        return reverse('category', kwargs={'slug': self.slug})


class Order(models.Model):
    """ Модель заказа """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(Product, through='Purchase', through_fields=('order', 'product'))
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата заказа')
    paid = models.BooleanField(default=False, verbose_name='оплачен')

    class Meta:
        db_table = 'orders'
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class Purchase(models.Model):
    """ Промежуточная модель для связи m2m order-product """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchases')
    quantity_of_product = models.PositiveIntegerField(default=0, verbose_name='количество товара')
    price_of_product = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='цена товара')


class Delivery(models.Model):
    """ Модель доставки заказа """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, unique=True)
    city = models.CharField(max_length=15, verbose_name='город')
    address = models.CharField(max_length=100, verbose_name='адрес')
    delivery_type = models.CharField(max_length=10, choices=[('simple', 'простая'), ('express', 'экспресс')],
                                     default='simple', verbose_name='тип доставки')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='стоимость доставки')


class CostOfDelivery(models.Model):
    """ Админ-параметры для доставки """
    price_simple = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='стоимость простой доставки')
    free_limit = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='бесплатно от')
    price_express = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='стоимость экспресс доставки')
