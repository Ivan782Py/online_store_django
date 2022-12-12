from django.db import models
from django.urls import reverse
from django.template.defaulttags import url


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


class Category(models.Model):
    """ Модель записи категорий товаров в БД """
    name = models.CharField(max_length=30, verbose_name='название')
    slug = models.SlugField(max_length=10, verbose_name='url')
    super_category = models.BooleanField(default=False, verbose_name='является родительской')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                               blank=True, verbose_name='родительская категория')
    favorites = models.BooleanField(default=False, verbose_name='избранное')
    image = models.FileField(upload_to='categories/', blank=True, null=True, help_text='only svg file!')

    class Meta:
        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> url:
        """ Абсолютный путь к объекту Category """
        return reverse('category', kwargs={'slug': self.slug})
