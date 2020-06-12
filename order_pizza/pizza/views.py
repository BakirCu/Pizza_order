from django.shortcuts import render, redirect
from .models import Cart, Product, CartProducts, Payment


def home(request):
    user = None
    cart = Cart.objects.create(user_id=user)
    request.session['cart_id'] = cart.id
    request.session['cart_items'] = 0
    return render(request, 'pizza/home.html')


def products(request):
    products_obj = Product.objects.all()
    cart_id = request.session.get("cart_id", None)
    return render(request, 'pizza/products.html', {'products': products_obj,
                                                   'cart': cart_id})


def cart_home(request):
    cart_id = request.session.get("cart_id", None)
    m = CartProducts.objects.filter(cart_id=cart_id)
    request.session['cart_items'] = len(m)
    products = CartProducts.objects.values('cart_id',
                                           'products_id',
                                           'quantity',
                                           'cart_id__total',
                                           'cart_id__delivery',
                                           'products_id__title',
                                           'products_id__price',
                                           ).filter(cart_id=cart_id)
    cart = Cart.objects.get(id=cart_id)

    return render(request, "pizza/cart.html", {"carts": products,
                                               "cart": cart})


def cart_add(request):
    cart_id = request.session.get("cart_id", None)
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    products_cart_update = CartProducts.objects.filter(cart_id=cart_id,
                                                       products_id=product_id)
    if not products_cart_update:
        add_to_card = CartProducts(quantity=quantity,
                                   cart_id=cart_id,
                                   products_id=product_id)
        add_to_card.save()
    else:
        add_to_card = CartProducts(id=products_cart_update.first().id,
                                   quantity=quantity, cart_id=cart_id, products_id=product_id)
        add_to_card.save()
    cart = Cart.objects.get(id=cart_id)
    total = cart.delivery
    p_k = CartProducts.objects.filter(cart_id=cart_id)
    request.session['cart_items'] = len(p_k)
    for product_k in p_k:
        product = Product.objects.get(id=product_k.products_id)
        total += product_k.quantity * product.price

    bill = Cart(id=cart.id, total=total,
                date_of_order=cart.date_of_order, user=cart.user)
    bill.save()
    return redirect('cart_home')


def cart_remove(request):
    cart_id = request.session.get("cart_id", None)
    product_id = request.POST.get('product_id')
    product_cart = CartProducts.objects.get(cart_id=cart_id,
                                            products_id=product_id)
    product_cart.delete()
    cart = Cart.objects.get(id=cart_id)
    total = cart.delivery
    p_k = CartProducts.objects.filter(cart_id=cart_id)
    request.session['cart_items'] = len(p_k)
    for product_k in p_k:
        product = Product.objects.get(id=product_k.products_id)
        total += product_k.quantity * product.price

    bill = Cart(id=cart.id, total=total,
                date_of_order=cart.date_of_order, user=cart.user)
    bill.save()
    return redirect('cart_home')


def order(request):
    if request.POST:
        cart_id = request.session.get("cart_id", None)
        cart = Cart.objects.get(id=cart_id)
        name = request.POST.get('Name')
        surname = request.POST.get('Surname')
        address = request.POST.get('Address')
        total = cart.total
        o = Payment(name=name, surname=surname,
                    address=address, bill=total)
        o.save()
        return redirect('home')
    return render(request, 'pizza/order.html')
