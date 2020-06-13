from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [path('', views.home, name='home'),
               path('products', views.products, name='products'),
               path('cart', views.cart_home, name='cart_home'),
               path('cart_add', views.cart_add, name='cart_add'),
               path('cart_remove', views.cart_remove, name='cart_remove'),
               path('order', views.order, name='order'),
               path('profile', views.profile, name='profile'),
               path('register', views.register, name='register'),
               path('login/', auth_views.LoginView.as_view(
                   template_name='pizza/login.html'), name='login'),
               path('logout/', auth_views.LogoutView.as_view(
                   template_name='pizza/logout.html'), name='logout'),
               ]
