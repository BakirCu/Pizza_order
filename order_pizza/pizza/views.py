from django.shortcuts import render, redirect
from .models import Cart, Product, CartProducts


def products(request):
    user = request.COOKIES['csrftoken']
    cart = Cart.objects.create(user=user)
    products_obj = Product.objects.all()
    return render(request, 'pizza/products.html', {'products': products_obj,
                                                   'cart': cart})


def cart_home(request, cart_id):
    print(cart_id)
    products = CartProducts.objects.values('card_id',
                                           'products_id',
                                           'quantity',
                                           'card_id__total',
                                           'card_id__delivery',
                                           'products_id__title',
                                           'products_id__price',
                                           ).filter(card_id=cart_id)
    cart = Cart.objects.get(id=cart_id)

    return render(request, "pizza/home.html", {"carts": products,
                                               "cart": cart})


def cart_add(request):
    product_id = request.POST.get('product_id')
    cart_id = request.POST.get('cart_id')
    quantity = request.POST.get('quantity')
    p_k = CartProducts.objects.filter(
        card_id=cart_id)
    products_cart = CartProducts.objects.filter(
        card_id=cart_id, products_id=product_id)
    if not products_cart:
        add_to_card = CartProducts(
            quantity=quantity, card_id=cart_id, products_id=product_id)
        add_to_card.save()
    else:
        add_to_card = CartProducts(id=products_cart.first().id,
                                   quantity=quantity, card_id=cart_id, products_id=product_id)
        add_to_card.save()
    cart = Cart.objects.get(id=cart_id)
    total = cart.delivery
    for product_k in p_k:
        product = Product.objects.get(id=product_k.products_id)
        total += product_k.quantity * product.price

    bill = Cart(id=cart.id, total=total,
                date_of_order=cart.date_of_order, user=cart.user)
    bill.save()
    return redirect('cart_home', cart_id=cart_id)
