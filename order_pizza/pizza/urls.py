from django.urls import path
from . import views


urlpatterns = [path('', views.products, name='products'),
               path('cart/<int:cart_id>/', views.cart_home, name='cart_home'),
               path('cart_add', views.cart_add, name='cart_add'),
               ]
