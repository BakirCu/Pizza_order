from django.shortcuts import render, redirect
from .models import Cart, Product


def products(request):
    products_obj = Product.objects.all()
    return render(request, 'pizza/products.html', {'products': products_obj})


def product(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    cart_obj = Cart.objects.new_or_get(request)
    return render(request, 'pizza/product.html', {'product': product_obj,
                                                  'cart': cart_obj})


def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    return render(request, "pizza/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id=product_id)
    cart_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart_home')
