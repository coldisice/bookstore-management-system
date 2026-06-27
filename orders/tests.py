from django.test import TestCase

from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse

from catalog.models import Author, Category, Book
from cart.models import Cart, CartItem
from .models import Order, OrderItem


class OrderTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='покупатель',
            password='TestPassword123!'
        )

        self.author = Author.objects.create(
            first_name='Лев',
            last_name='Толстой'
        )

        self.category = Category.objects.create(
            name='Роман'
        )

        self.book = Book.objects.create(
            title='Война и мир',
            isbn='9785170901234',
            description='Русский роман',
            price=Decimal('1500.00'),
            stock_quantity=5,
            publication_date=date(1869, 1, 1)
        )

        self.book.authors.add(self.author)
        self.book.categories.add(self.category)

    def test_order_list_requires_login(self):
        response = self.client.get(
            reverse('order_list')
        )

        self.assertEqual(response.status_code, 302)

    def test_create_order(self):
        self.client.login(
            username='покупатель',
            password='TestPassword123!'
        )

        cart = Cart.objects.create(
            user=self.user
        )

        CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=2
        )

        self.client.get(
            reverse('create_order')
        )

        self.assertEqual(
            Order.objects.count(),
            1
        )

    def test_order_item_created(self):
        self.client.login(
            username='покупатель',
            password='TestPassword123!'
        )

        cart = Cart.objects.create(
            user=self.user
        )

        CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=2
        )

        self.client.get(
            reverse('create_order')
        )

        self.assertEqual(
            OrderItem.objects.count(),
            1
        )

    def test_cart_cleared_after_order(self):
        self.client.login(
            username='покупатель',
            password='TestPassword123!'
        )

        cart = Cart.objects.create(
            user=self.user
        )

        CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=2
        )

        self.client.get(
            reverse('create_order')
        )

        self.assertEqual(
            cart.items.count(),
            0
        )

    def test_order_total_price(self):
        self.client.login(
            username='покупатель',
            password='TestPassword123!'
        )

        cart = Cart.objects.create(
            user=self.user
        )

        CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=2
        )

        self.client.get(
            reverse('create_order')
        )

        order = Order.objects.first()

        self.assertEqual(
            order.total_price,
            Decimal('3000.00')
        )

    def test_order_detail_page(self):
        self.client.login(
            username='покупатель',
            password='TestPassword123!'
        )

        order = Order.objects.create(
            user=self.user,
            total_price=Decimal('1000.00')
        )

        response = self.client.get(
            reverse(
                'order_detail',
                args=[order.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )
