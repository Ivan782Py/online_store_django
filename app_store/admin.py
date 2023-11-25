from django.contrib import admin

from app_store.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Админ-интерфейс товара """
    list_display = ['name', 'count', 'price', 'category', 'status']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Админ-интерфейс категории товара """
    list_display = ['name', 'slug', 'parent', 'changed_in']
