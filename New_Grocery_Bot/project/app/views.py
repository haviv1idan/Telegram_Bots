from rest_framework import generics
from .models import Product, Shop, OnlineShop, User, Message
from .serializers import ProductSerializer, ShopSerializer, OnlineShopSerializer, UserSerializer, MessageSerializer

__all__ = [
    'ProductGetView', 'ProductCreateView', 'ProductUpdateView', 'ProductDeleteView',
    'ShopGetView', 'ShopCreateView', 'ShopUpdateView', 'ShopDeleteView',
    'OnlineShopGetView', 'OnlineShopCreateView', 'OnlineShopUpdateView', 'OnlineShopDeleteView',
    'UserGetView', 'UserCreateView', 'UserUpdateView', 'UserDeleteView',
    'MessageGetView', 'MessageCreateView', 'MessageUpdateView', 'MessageDeleteView',
]

# Create your views here.
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


class UserGetView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageGetView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDeleteView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
