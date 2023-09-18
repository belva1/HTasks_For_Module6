from .models import Book
from .serializers import BookSerializer

from rest_framework import viewsets
from rest_framework.decorators import authentication_classes

from rest_framework.authentication import SessionAuthentication
from users.authentication import CustomTokenAuthentication
from users.permissions import IsAdminCreateOrAuthenticated

from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import IsAuthorFilterBackend, AuthorBooksByAgeFilterBackend


@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminCreateOrAuthenticated]
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        IsAuthorFilterBackend,
        AuthorBooksByAgeFilterBackend
    ]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(title=serializer.validated_data['title'] + '!')
