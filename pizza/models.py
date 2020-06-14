from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=50)
    date_of_order = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, null=True,
                             blank=True,
                             on_delete=models.CASCADE)
    delivery = models.DecimalField(
        decimal_places=2, max_digits=50, default='1.00')
    total = models.DecimalField(
        decimal_places=2, max_digits=50, default='0.00')
    date_of_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default='1')

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    bill = models.DecimalField(decimal_places=2, max_digits=50)

    def __str__(self):
        return str(self.name)
