from django.test import TestCase
from .models import Book
from authors.models import Author


class BookModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Selena Phil', age='30')
        self.book = Book.objects.create(title='St. Mark', author=self.author)

    def test_author_book(self):
        book = Book.objects.first()
        self.assertEqual(book.author, self.author)

    def test_book_str(self):
        str_book = 'St. Mark'
        self.assertEqual(str(self.book), str_book)


class BookIntegrationTestCase(TestCase):
    def test_create_book_with_author(self):
        author = Author.objects.create(name='Layla Tbili', age='29')
        book = Book.objects.create(title='LiLi', author=author)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(book.author, author)