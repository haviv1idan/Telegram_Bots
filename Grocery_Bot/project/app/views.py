# myapp/views.py

from rest_framework import generics
from .models import Product, Shop, OnlineShop
from .serializers import ProductSerializer, ShopSerializer, OnlineShopSerializer


class ProductGetView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShopGetView(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ShopCreateView(generics.CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ShopUpdateView(generics.UpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ShopDeleteView(generics.DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class OnlineShopGetView(generics.ListAPIView):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer


class OnlineShopCreateView(generics.CreateAPIView):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer


class OnlineShopUpdateView(generics.UpdateAPIView):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer


class OnlineShopDeleteView(generics.DestroyAPIView):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer
