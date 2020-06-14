from django.contrib import admin
from .models import Product, Cart, Order, CartProducts


admin.site.register([Product, Cart, Order, CartProducts])
