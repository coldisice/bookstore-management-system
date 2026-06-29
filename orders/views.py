from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from cart.models import Cart
from .models import Order, OrderItem


@login_required
def create_order(request):

    cart = Cart.objects.get(
        user=request.user
    )

    if not cart.items.exists():
        return redirect('cart_detail')

    unavailable_books = []

    for item in cart.items.all():
        if item.quantity > item.book.stock_quantity:

            unavailable_books.append(
                f'{item.book.title} '
                f'(доступно: {item.book.stock_quantity}, '
                f'в корзине: {item.quantity})'
            )

    if unavailable_books:
        messages.error(
            request,
            "Невозможно оформить заказ. Недостаточно товаров на складе:<br>"
            + "<br>".join(unavailable_books)
        )
        return redirect("cart_detail")

    order = Order.objects.create(
        user=request.user,
        total_price=Decimal('0.00')
    )

    total_price = Decimal('0.00')

    for item in cart.items.all():

        item_total = (
            item.book.price *
            item.quantity
        )

        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )
        item.book.stock_quantity -= item.quantity
        item.book.save(update_fields=["stock_quantity"])

        total_price += item_total

    order.total_price = total_price
    order.save

    cart.items.all().delete()

    return redirect(
        'order_detail',
        order_id=order.id
    )


@login_required
def order_list(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/order_list.html',
        {
            'orders': orders
        }
    )


@login_required
def order_detail(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )
