from django.contrib import admin
from .models import Product, Shop, OnlineShop, User, Message


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode')
    list_filter = ('name', 'barcode')

class ShopAdmin(admin.ModelAdmin):
    list_display = ('chain', 'name', 'address', 'distance', 'sale', 'price', 'barcode')
    list_filter = ('chain', 'name', 'address', 'distance', 'sale', 'price', 'barcode')


class OnlineShopAdmin(admin.ModelAdmin):
    list_display = ('chain', 'name', 'website', 'sale', 'price', 'barcode')
    list_filter = ('chain', 'name', 'website', 'sale', 'price', 'barcode')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'first_name', 'last_name', 'language_code')
    list_filter = ('id', 'name', 'first_name', 'last_name', 'language_code') 
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'unix_time', 'is_bot', 'user_id')
    list_filter = ('id', 'text', 'unix_time', 'is_bot', 'user_id')


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(OnlineShop, OnlineShopAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
