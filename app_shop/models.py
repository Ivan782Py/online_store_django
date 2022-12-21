from django.db import models
from django.urls import reverse
from django.template.defaulttags import url
from django.contrib.auth.models import User


class Product(models.Model):
    """ Модель записи товаров в БД """
    PRODUCT_STATUS = [
        ('limited', 'Ограниченный тираж'),
        ('top', 'Топ продаж'),
        ('sale', 'Распродажа'),
        ('default', 'Стандарт'),
    ]
    name = models.CharField(max_length=200, verbose_name='название')
    count = models.PositiveIntegerField(default=1, blank=True, verbose_name='количество')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='цена')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,
                                 related_name='products', verbose_name='Категория')
    description = models.TextField(max_length=5000, verbose_name='описание')
    status = models.SlugField(max_length=10, choices=PRODUCT_STATUS, default='default', verbose_name='статус')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата поступления')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> url:
        """ Абсолютный путь к объекту Product """
        return reverse('product', kwargs={'pk': self.id, 'slug': self.status})

    def get_descr(self) -> str:
        """ Сократить длинное описание """
        if len(self.description) > 50:
            return self.description[:45] + '...'
        return self.description


class Category(models.Model):
    """ Модель записи категорий товаров в БД """
    name = models.CharField(max_length=30, verbose_name='название')
    slug = models.SlugField(max_length=10, verbose_name='url')
    super_category = models.BooleanField(default=False, verbose_name='является родительской')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                               blank=True, verbose_name='родительская категория')
    favorites = models.BooleanField(default=False, verbose_name='избранное')
    image = models.FileField(upload_to='categories/', blank=True, null=True, help_text='only svg file!')
    changed_in = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> url:
        """ Абсолютный путь к объекту Category """
        return reverse('category', kwargs={'slug': self.slug})


class Order(models.Model):
    """ Модель записи заказов в БД """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    items = models.ManyToManyField(Product, through='Purchase', through_fields=('order', 'product'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата покупки')

    class Meta:
        db_table = 'order'
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class Purchase(models.Model):
    """ Промежуточная модель для связи m2m Order - Product """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    quantity_of_product = models.PositiveIntegerField(default=0)
    price_of_product = models.DecimalField(max_digits=9, decimal_places=2)
