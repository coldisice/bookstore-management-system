from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Author, Category, Book


class AuthorModelTest(TestCase):

    def test_author_creation(self):
        author = Author.objects.create(
            first_name='Джордж',
            last_name='Оруэлл',
            biography='Британский писатель'
        )

        self.assertEqual(author.first_name, 'Джордж')
        self.assertEqual(author.last_name, 'Оруэлл')

    def test_author_str(self):
        author = Author.objects.create(
            first_name='Джордж',
            last_name='Оруэлл'
        )

        self.assertEqual(
            str(author),
            'Джордж Оруэлл'
        )


class CategoryModelTest(TestCase):

    def test_category_creation(self):
        category = Category.objects.create(
            name='Роман',
            description='Художественная литература'
        )

        self.assertEqual(category.name, 'Роман')

    def test_category_str(self):
        category = Category.objects.create(
            name='Роман'
        )

        self.assertEqual(
            str(category),
            'Роман'
        )


class BookModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name='Джордж',
            last_name='Оруэлл'
        )

        self.category = Category.objects.create(
            name='Роман'
        )

    def test_book_creation(self):
        book = Book.objects.create(
            title='1984',
            isbn='9780451524935',
            description='Роман-антиутопия',
            price=340,
            stock_quantity=10,
            publication_date=date(1949, 6, 8)
        )

        book.authors.add(self.author)
        book.categories.add(self.category)

        self.assertEqual(book.title, '1984')
        self.assertEqual(book.isbn, '9780451524935')

    def test_book_str(self):
        book = Book.objects.create(
            title='1984',
            isbn='9780451524935',
            description='Роман-антиутопия',
            price=340,
            stock_quantity=10,
            publication_date=date(1949, 6, 8)
        )

        self.assertEqual(
            str(book),
            '1984'
        )

    def test_book_relations(self):
        book = Book.objects.create(
            title='1984',
            isbn='9780451524935',
            description='Роман-антиутопия',
            price=340,
            stock_quantity=10,
            publication_date=date(1949, 6, 8)
        )

        book.authors.add(self.author)
        book.categories.add(self.category)

        self.assertEqual(
            book.authors.count(),
            1
        )

        self.assertEqual(
            book.categories.count(),
            1
        )


class CatalogViewsTest(TestCase):

    def setUp(self):
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
            description='Роман',
            price=400,
            stock_quantity=5,
            publication_date=date(1869, 1, 1)
        )

        self.book.authors.add(self.author)
        self.book.categories.add(self.category)

    def test_book_list_page(self):
        response = self.client.get(
            reverse('book_list')
        )

        self.assertEqual(response.status_code, 200)

    def test_book_list_contains_book(self):
        response = self.client.get(
            reverse('book_list')
        )

        self.assertContains(
            response,
            'Война и мир'
        )

    def test_book_detail_page(self):
        response = self.client.get(
            reverse('book_detail', args=[self.book.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_book_detail_contains_title(self):
        response = self.client.get(
            reverse('book_detail', args=[self.book.pk])
        )

        self.assertContains(
            response,
            'Война и мир'
        )
