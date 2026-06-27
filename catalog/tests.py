from datetime import date

from django.test import TestCase

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