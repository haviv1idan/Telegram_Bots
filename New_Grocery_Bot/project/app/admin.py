from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode')
    list_filter = ('name', 'barcode')

# Register your models here.
admin.site.register(Product, ProductAdmin)
