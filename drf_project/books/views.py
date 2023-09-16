from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, viewsets
from rest_framework.decorators import action, authentication_classes
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication
from drf_project.authentication import CustomTokenAuthentication
from drf_project.permissions import IsAdminCreateOrAuthenticated

from .filters import IsAuthorFilterBackend
from .models import Book
from .serializers import BookSerializer


@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminCreateOrAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, IsAuthorFilterBackend]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(title=serializer.validated_data['title'] + '!')

    @action(detail=False, methods=['GET'])
    def get_books_by_author_age(self, request):
        author_age = request.query_params.get('author_age')

        if author_age:
            try:
                author_age = int(author_age)
            except ValueError:
                return Response({"error": "Invalid author_age parameter"}, status=status.HTTP_400_BAD_REQUEST)

            books = Book.objects.filter(author__age__gte=author_age)
        else:
            books = Book.objects.all()

        ser_books = BookSerializer(books, many=True)
        return Response(data=ser_books.data, status=status.HTTP_200_OK)