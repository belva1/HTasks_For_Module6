from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    """
    Override the save method to add an exclamation mark before saving.
    """
    def save(self, **kwargs):
        self.validated_data['title'] += '!'
        return super().save(**kwargs)

