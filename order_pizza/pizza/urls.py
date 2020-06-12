from django.urls import path
from . import views


urlpatterns = [path('', views.home, name='home'),
               path('products', views.products, name='products'),
               path('cart', views.cart_home, name='cart_home'),
               path('cart_add', views.cart_add, name='cart_add'),
               path('cart_remove', views.cart_remove, name='cart_remove'),
               path('order', views.order, name='order'),
               ]
