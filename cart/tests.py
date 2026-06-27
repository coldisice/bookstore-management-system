from django.test import TestCase

from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse

from catalog.models import Author, Category, Book
from .models import Cart, CartItem


class CartTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='читатель',
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
            price=1500,
            stock_quantity=5,
            publication_date=date(1869, 1, 1)
        )

        self.book.authors.add(self.author)
        self.book.categories.add(self.category)

    def test_cart_requires_login(self):
        response = self.client.get(
            reverse('cart_detail')
        )

        self.assertEqual(response.status_code, 302)

    def test_add_book_to_cart(self):
        self.client.login(
            username='читатель',
            password='TestPassword123!'
        )

        self.client.get(
            reverse('add_to_cart', args=[self.book.id])
        )

        cart = Cart.objects.get(user=self.user)

        self.assertEqual(
            cart.items.count(),
            1
        )

    def test_increase_quantity(self):
        self.client.login(
            username='читатель',
            password='TestPassword123!'
        )

        self.client.get(
            reverse('add_to_cart', args=[self.book.id])
        )

        self.client.get(
            reverse('add_to_cart', args=[self.book.id])
        )

        item = CartItem.objects.get(
            cart__user=self.user
        )

        self.assertEqual(item.quantity, 2)

    def test_update_cart_item_increase(self):
        self.client.login(
            username='читатель',
            password='TestPassword123!'
        )

        cart = Cart.objects.create(
            user=self.user
        )

        item = CartItem.objects.create(
            cart=cart,
            book=self.book,
            quantity=1
        )

        self.client.get(
            reverse(
                'update_cart_item',
                args=[item.id, 'increase']
            )
        )

        item.refresh_from_db()

        self.assertEqual(item.quantity, 2)

    def test_remove_cart_item(self):
        self.client.login(
            username='читатель',
            password='TestPassword123!'
        )

        cart = Cart.objects.create(
            user=self.user
        )

        item = CartItem.objects.create(
            cart=cart,
            book=self.book
        )

        self.client.get(
            reverse(
                'remove_cart_item',
                args=[item.id]
            )
        )

        self.assertFalse(
            CartItem.objects.filter(
                id=item.id
            ).exists()
        )
