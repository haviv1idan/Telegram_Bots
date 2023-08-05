# myapp/urls.py

from django.urls import path
from .views import ProductGetView, ProductCreateView, ProductUpdateView, ProductDeleteView
from .views import ShopGetView, ShopCreateView, ShopUpdateView, ShopDeleteView

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
    path('OnlineShop/get/', ShopGetView.as_view(), name='OnlineShop-get'),
    path('OnlineShop/create/', ShopCreateView.as_view(), name='OnlineShop-create'),
    path('OnlineShop/update/<int:pk>/', ShopUpdateView.as_view(), name='OnlineShop-update'),
    path('OnlineShop/delete/<int:pk>/', ShopDeleteView.as_view(), name='OnlineShop-delete'),
]
