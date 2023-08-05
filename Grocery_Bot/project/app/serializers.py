# myapp/serializers.py

from rest_framework import serializers
from .models import Product, Shop, OnlineShop


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class OnlineShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineShop
        fields = '__all__'
