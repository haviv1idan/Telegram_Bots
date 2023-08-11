# myapp/urls.py

from django.urls import path
from .views import *


urlpatterns = [
    # Product api
    path('product/get/', ProductGetView.as_view(), name='Product-get'),
    path('product/create/', ProductCreateView.as_view(), name='Product-create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='Product-update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='Product-delete'),

    # Shop api
    path('shop/get/', ShopGetView.as_view(), name='Shop-get'),
    path('shop/create/', ShopCreateView.as_view(), name='Shop-create'),
    path('shop/update/<int:pk>/', ShopUpdateView.as_view(), name='Shop-update'),
    path('shop/delete/<int:pk>/', ShopDeleteView.as_view(), name='Shop-delete'),

    # OnlineShop api
    path('OnlineShop/get/', OnlineShopGetView.as_view(), name='OnlineShop-get'),
    path('OnlineShop/create/', OnlineShopCreateView.as_view(), name='OnlineShop-create'),
    path('OnlineShop/update/<int:pk>/', OnlineShopUpdateView.as_view(), name='OnlineShop-update'),
    path('OnlineShop/delete/<int:pk>/', OnlineShopDeleteView.as_view(), name='OnlineShop-delete'),
 
    # User api
    path('user/get/', UserGetView.as_view(), name='user-get'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
 
    # Message api
    path('message/get/', MessageGetView.as_view(), name='message-get'),
    path('message/create/', MessageCreateView.as_view(), name='message-create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message-delete'),
]
