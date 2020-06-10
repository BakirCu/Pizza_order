from django.urls import path
from . import views


urlpatterns = [path('', views.products, name='products'),
               path('product/<int:product_id>/',
                    views.product, name='product'),
               path('card', views.cart_home, name='cart_home'),
               path('card_update', views.cart_update, name='cart_update'),
               ]
