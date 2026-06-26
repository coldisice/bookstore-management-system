from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required

from catalog.models import Book
from .models import Cart, CartItem

@login_required
def add_to_cart(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    total = 0

    for item in cart.items.all():
        total += item.book.price * item.quantity

    return render(
        request,
        'cart/cart_detail.html',
        {
            'cart': cart,
            'total': total,
        }
    )

@login_required
def update_cart_item(request, item_id, action):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if action == "increase":
        item.quantity += 1
        item.save()

    elif action == "decrease":
        item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

    return redirect('cart_detail')


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect('cart_detail')