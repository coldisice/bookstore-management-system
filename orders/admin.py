from django.contrib import admin
from django import forms

from .models import Order, OrderItem, Book

from django.http import JsonResponse
from django.urls import path


class OrderItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["price"].widget.attrs["readonly"] = True
        self.fields["price"].required = False


class OrderItemInline(admin.TabularInline):

    model = OrderItem
    form = OrderItemAdminForm
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = [
        OrderItemInline
    ]

    class Media:
        js = (
            "orders/js/order_admin.js",
        )

    list_display = (
        'id',
        'user',
        'status',
        'total_price',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'user__username',
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "book-price/<int:book_id>/",
                self.admin_site.admin_view(self.book_price),
                name="order_book_price"
            )
        ]

        return custom_urls + urls

    def book_price(self, request, book_id):
        book = Book.objects.get(pk=book_id)

        return JsonResponse({
            "price": str(book.price)
        })

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        order = form.instance

        order.total_price = sum(
            item.price * item.quantity
            for item in order.items.all()
        )

        order.save(update_fields=["total_price"])


# admin.site.register(OrderItem)
