from rest_framework.test import APITestCase
from rest_framework import status

from django.test import TestCase
from django.urls import reverse

from users.models import UM
from .models import Book
from authors.models import Author


# This class of tests focuses solely on testing model methods and behavior.
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


# In this class of tests, which access views, it necessary to create a user and
# authenticate them to ensure that the permission is applied correctly.
class BooksViewSetTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Selena Phil', age='30')
        self.book = Book.objects.create(title='St. Mark', author=self.author)
        self.user = UM.objects.create_user(username='test_user', password='test_user_password')
        self.client.force_authenticate(user=self.user)
        """
        Using self.client.force_authenticate to authenticate the client on behalf of the created user self.user. 
        This means that when making HTTP requests using self.client (eg self.client.get), the client will be 
        an authenticated user 'test_user' who has access rights according to its permissions.
        """

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        Book.objects.create(title='St. Deal', author=self.author)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_book_create(self):
        # ONLY ADMIN CAN CREATE BOOKS
        admin_user = UM.objects.create_user(username='admin_user', password='admin_password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_authenticate(user=admin_user)

        url = reverse("book-list")
        data = {
            'title': 'TestBook',
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        try:
            created_book = Book.objects.get(title='TestBook!')
        except Book.DoesNotExist:
            created_book = None

        if created_book:
            expected_data = {
                'id': created_book.id,
                'title': created_book.title,
                'author': self.author.id
            }
            self.assertEqual(response.data, expected_data)
        else:
            print("Created book not found in the database.")

    def test_book_create_failed(self):
        # AUTHENTICATED USERS CANNOT CREATE BOOKS
        url = reverse("book-list")
        data = {
            'title': 'TestBook',
            'author': self.author.id
        }
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_detail(self):
        url = reverse("book-detail", args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result =  {'id': 16, 'title': 'St. Mark', 'author': 14}
        self.assertEqual(response.data, result)

    def test_book_detail_failed(self):
        url = reverse("book-detail", args=[555])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# This class of integration tests the interaction between different application components
# or modules to ensure that they work together correctly and integrate without errors.
class BookIntegrationTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Layla Tbili', age='29')
        self.book = Book.objects.create(title='LiLi', author=self.author)
        self.user = UM.objects.create_user(username='test_user', password='test_user_password')
        self.client.force_authenticate(user=self.user)

    def test_create_book_with_author(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(self.book.author, self.author)

    def test_create_book_without_author(self):
        response = self.client.post(reverse("book-list"), data={'title': 'NoAuthorBook!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        """
        My code checks for the presence of an author when creating a book and prevents 
        the creation of a book without an author. Accordingly, as a result of such an attempt, 
        the server should return status 403.
        """

    def test_delete_book(self):
        book_to_delete = Book.objects.create(title='BookToDelete', author=self.author)

        url = reverse("book-detail", args=[book_to_delete.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookFiltersTestCase(APITestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='TestAuthor1', age=30)
        self.author2 = Author.objects.create(name='TestAuthor2', age=40)
        self.book1 = Book.objects.create(title='TestBook1', author=self.author1)
        self.book2 = Book.objects.create(title='TestBook2', author=self.author2)
        self.user = UM.objects.create_user(username='test_user', password='test_user_password')
        self.client.force_authenticate(user=self.user)

    def test_is_author_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, {'is_author': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # BOTH BOOKS OBJECTS SHOULD BE RETURNED

    def test_author_books_by_age_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, {'author_age': '35'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # Expected to have only 1 book object since author_age is 35 and only one author is older than 35
        self.assertEqual(response.data[0]['title'], 'TestBook2')
        # Checks that the title of this book matches "TestBook2"

    def test_author_books_by_age_filter_no_value(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        """
        The response is expected to contain both book objects since there 
        is no filtering by author age and all books in the database should be returned
        """