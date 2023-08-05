from django.contrib import admin
from .models import Product, Shop, OnlineShop


class ProductAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name')
    list_filter = ('barcode',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('chain', 'name', 'address', 'distance', 'sale', 'price', 'barcode')
    list_filter = ('chain', 'name', 'address', 'distance', 'sale', 'price', 'barcode')


class OnlineShopAdmin(admin.ModelAdmin):
    list_display = ('chain', 'name', 'website', 'sale', 'price', 'barcode')
    list_filter = ('chain', 'name', 'website', 'sale', 'price', 'barcode')


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(OnlineShop, OnlineShopAdmin)
