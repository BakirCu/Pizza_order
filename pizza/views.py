from django.shortcuts import render, redirect
from .models import Cart, Product, CartProducts, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, OrderForm
from .my_functions import bill_update


def home(request):
    if request.user.is_authenticated:
        user = request.user.id
    else:
        user = None
    cart = Cart.objects.create(user_id=user)
    request.session['cart_id'] = cart.id
    request.session['cart_items'] = 0
    return render(request, 'pizza/home.html')


def products(request):
    products_obj = Product.objects.all()
    cart_id = request.session.get("cart_id", None)
    if not cart_id:
        messages.success(request, 'Create cart first')
        return redirect('home')
    return render(request, 'pizza/products.html', {'products': products_obj,
                                                   'cart': cart_id})


def cart_home(request):
    cart_id = request.session.get("cart_id", None)
    if not cart_id:
        messages.success(request, 'Create cart first')
        return redirect('home')
    cart_items = CartProducts.objects.filter(cart_id=cart_id)
    request.session['cart_items'] = len(cart_items)
    cart_products = CartProducts.objects.values('cart_id',
                                                'products_id',
                                                'quantity',
                                                'cart_id__total',
                                                'cart_id__delivery',
                                                'products_id__title',
                                                'products_id__price',
                                                ).filter(cart_id=cart_id)
    cart = Cart.objects.get(id=cart_id)
    return render(request, "pizza/cart.html", {"carts": cart_products,
                                               "cart": cart})


def cart_add(request):
    cart_id = request.session.get("cart_id", None)
    if not cart_id:
        messages.success(request, 'Create cart first')
        return redirect('home')
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    if not product_id or not quantity or isinstance(product_id, int) or isinstance(quantity, int) or int(quantity) < 0:
        messages.success(request, 'Inesert only positive number!')
        return redirect('home')
    cart_products_update = CartProducts.objects.filter(cart_id=cart_id,
                                                       products_id=product_id)
    if not cart_products_update:
        add_to_card = CartProducts(quantity=quantity,
                                   cart_id=cart_id,
                                   products_id=product_id)
        add_to_card.save()
    else:
        add_to_card = CartProducts(id=cart_products_update.first().id,
                                   quantity=quantity,
                                   cart_id=cart_id,
                                   products_id=product_id)
        add_to_card.save()
    bill_update(request, cart_id)
    return redirect('cart_home')


def cart_remove(request):
    cart_id = request.session.get("cart_id", None)
    if not cart_id:
        messages.success(request, 'Create cart first')
        return redirect('home')
    product_id = request.POST.get('product_id')
    if not product_id or isinstance(product_id, int) or int(product_id) < 1:
        messages.success(request, 'Inesert only positive number!')
        return redirect('home')
    product_cart = CartProducts.objects.get(cart_id=cart_id,
                                            products_id=product_id)
    product_cart.delete()
    bill_update(request, cart_id)
    return redirect('cart_home')


def order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            cart_id = request.session.get("cart_id", None)
            cart = Cart.objects.get(id=cart_id)
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            address = form.cleaned_data["address"]
            total = cart.total
            order = Order(name=name, surname=surname,
                          address=address, bill=total)
            order.save()
            messages.success(request, 'Order succeeded')
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'pizza/order.html', {'order_form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'pizza/register.html', {'form': form})


@login_required(login_url='/login/')
def profile(request):
    user_id = request.user.id
    carts = Cart.objects.filter(user_id=user_id).order_by('-date_of_order')
    return render(request, 'pizza/profile.html', {'carts': carts})
