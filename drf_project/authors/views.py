from rest_framework import status, viewsets
from rest_framework.decorators import action, authentication_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.authentication import SessionAuthentication
from drf_project.authentication import CustomTokenAuthentication

from .models import Author
from .serializers import AuthorSerializer
from drf_project.permissions import IsAdminCreateOrAuthenticated


@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminCreateOrAuthenticated]


    def get_queryset(self):
        queryset = Author.objects.all()
        book_name = self.request.query_params.get('book_name')

        if book_name:
            queryset = queryset.filter(author_of_books__title__icontains=book_name)

        return queryset

    @action(detail=True, methods=['GET'])
    def author_with_books(self, request, pk=None):
        author = self.get_object()

        author_data = {
            'id': author.id,
            'name': author.name,
            'age': author.age,
            'books': author.get_id_of_books(),
        }

        return Response(data=author_data, status=status.HTTP_200_OK)