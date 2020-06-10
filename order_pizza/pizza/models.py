from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed
from decimal import Decimal
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            if cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:

            user_obj = user
        return self.model.objects.create(user=user_obj)


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=50)
    date_of_order = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(
        decimal_places=2, max_digits=50, default='0.00')
    total = models.DecimalField(
        decimal_places=2, max_digits=50, default='0.00')
    date_of_order = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08)  # 8% tax
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
