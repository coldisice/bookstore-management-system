from django.contrib import admin

from .models import Cart, CartItem

# admin.site.register(Cart)
# admin.site.register(CartItem)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
    )

    search_fields = (
        'user__username',
    )

    list_select_related = (
        'user',
    )

    inlines = [
        CartItemInline,
    ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'book',
        'quantity',
    )

    list_select_related = (
        'cart',
        'book',
    )

    search_fields = (
        'cart__user__username',
        'book__title',
    )
