from django.contrib import admin

from app_shop.models import Product, Category, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Админка для товаров """
    list_display = ('id', 'name', 'category', 'count', 'price', 'status')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Админка для категорий """
    list_display = ('id', 'name', 'parent', 'super_category', 'favorites')


class PurchaseInline(admin.TabularInline):
    model = Order.items.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Админка для тестового создания заказов """
    exclude = ('id',)
    inlines = [PurchaseInline, ]
