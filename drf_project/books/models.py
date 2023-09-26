from django.db import models
from authors.models import Author


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='author_of_books', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title
