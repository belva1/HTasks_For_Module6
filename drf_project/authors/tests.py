from rest_framework.test import APITestCase
from rest_framework import status

from django.test import TestCase
from django.urls import reverse

from users.models import UM
from .models import Author
from books.models import Book


# This class of tests focuses solely on testing model methods and behavior.
class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Suzy Mol', age='20')

    def test_author(self):
        author = Author.objects.first()
        self.assertEqual(author, self.author)

    def test_author_str(self):
        author_name = 'Suzy Mol'
        self.assertEqual(self.author.name, author_name)


# In this class of tests, which access views, it necessary to create a user and
# authenticate them to ensure that the permission is applied correctly.
class AuthorsViewSetTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Suzy Mol', age='20')
        self.user = UM.objects.create_user(username='test_user', password='test_user_password')
        self.client.force_authenticate(user=self.user)
        """
        Using self.client.force_authenticate to authenticate the client on behalf of the created user self.user.
        This means that when making HTTP requests using self.client (eg self.client.get), the client will be
        an authenticated user 'test_user' who has access rights according to its permissions.
        """

    def test_list_authors(self):
        url = reverse("author-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        Author.objects.create(name='Selena Deal', age=self.author.age)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_author_create(self):
        # ONLY ADMIN CAN CREATE AUTHORS
        admin_user = UM.objects.create_user(username='admin_user', password='admin_password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_authenticate(user=admin_user)

        url = reverse("author-list")
        data = {
            'name': 'TestAuthor',
            'age': int(self.author.age)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        try:
            created_author = Author.objects.get(name='TestAuthor')
        except Author.DoesNotExist:
            created_author = None

        if created_author:
            expected_data = {
                'id': created_author.id,
                'name': created_author.name,
                'age': int(created_author.age)
            }
            self.assertEqual(response.data, expected_data)
        else:
            print("Created author not found in the database.")

    def test_book_create_failed(self):
        # AUTHENTICATED USERS CANNOT CREATE AUTHORS
        url = reverse("author-list")
        data = {
            'name': 'TestAuthor',
            'age': int(self.author.age)
        }
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_detail(self):
        url = reverse("author-detail", args=[self.author.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_detail_failed(self):
        url = reverse("author-detail", args=[555])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# This class of integration tests the interaction between different application components
# or modules to ensure that they work together correctly and integrate without errors.
class AuthorsViewSetIntegrationTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Layla Tbili', age='29')
        self.user = UM.objects.create_user(username='test_user', password='test_user_password')
        self.client.force_authenticate(user=self.user)

    def test_author_with_books(self):
        url = reverse("author-author-with-books", args=[self.author.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': self.author.pk,
            'name': self.author.name,
            'age': int(self.author.age),
            'books': self.author.get_id_of_books(),
        }
        self.assertEqual(response.data, expected_data)

    def test_author_with_books_nonexistent_author(self):
        url = reverse("author-author-with-books", args=[55])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookNameFilterTestCase(APITestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='TestAuthor1', age=30)
        self.author2 = Author.objects.create(name='TestAuthor2', age=40)
        self.book1 = Book.objects.create(title='TestBook1', author=self.author1)
        self.book2 = Book.objects.create(title='TestBook2', author=self.author2)
        self.user = UM.objects.create_user(username='test_user', password='test_user_password')
        self.client.force_authenticate(user=self.user)

    def test_book_name_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, {'book_name': 'TestBook1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        """
        Could you please tell me why all objects are returned if I filter by book_name?
        In the written filters with author_age everything worked for me.
        
        There is failed testing.
        """
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'TestBook1')

    # def test_book_name_filter_no_match(self):
    #     url = reverse('book-list')
    #     response = self.client.get(url, {'book_name': 'Nonexistent Book'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 0)
    #
    # def test_book_name_filter_no_value(self):
    #     url = reverse('book-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 2)
