from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from orders.models import Order


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )


@login_required
def profile(request):

    orders_count = Order.objects.filter(
        user=request.user
    ).count()

    cart_items_count = 0

    try:
        cart = Cart.objects.get(
            user=request.user
        )

        cart_items_count = cart.items.count()

    except Cart.DoesNotExist:
        pass

    return render(
        request,
        'users/profile.html',
        {
            'orders_count': orders_count,
            'cart_items_count': cart_items_count,
        }
    )
