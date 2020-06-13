from .models import Cart, Product, CartProducts


def bill_update(request, cart_id):

    cart = Cart.objects.get(id=cart_id)
    total = cart.delivery
    cart_items = CartProducts.objects.filter(cart_id=cart_id)
    request.session['cart_items'] = len(cart_items)
    for cart_item in cart_items:
        product = Product.objects.get(id=cart_item.products_id)
        total += cart_item.quantity * product.price
        bill = Cart(id=cart.id, total=total,
                    date_of_order=cart.date_of_order, user=cart.user)
        bill.save()
