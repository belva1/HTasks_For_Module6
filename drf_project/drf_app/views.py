from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


@api_view(['GET', 'POST'])
def books_list_view(request) -> Response:
    if request.method == 'GET':
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

    if request.method == 'POST':
        # immediately create a serializer with transmitted data
        ser_book = BookSerializer(data=request.data)
        # then, it necessary to check validation of the serializer
        if ser_book.is_valid():
            ser_book.validated_data['title'] += '!'
            ser_book.save()
            return Response(data=ser_book.data, status=status.HTTP_201_CREATED)
        return Response(ser_book.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def books_detail_view(request, pk) -> Response:

    """
    instead of Book.objects.get(pk=pk) I use Book.objects.filter(pk=pk).first() :
    If this object does not exist, instead of throwing an "DoesNotExist" error, my condition block will go
    to return Response(status=status.HTTP_404_NOT_FOUND), because object WO this pk will return "None".

    This can also be implemented using Book.objects.get(pk=pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    """

    book = Book.objects.filter(pk=pk).first()
    if book:
        if request.method == 'GET':
            ser_book = BookSerializer(book)
            return Response(data=ser_book.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        """
        Combined the logic for PUT and PATCH requests in one block. 
        Use request.method == 'PATCH' to determine if the request is a 
        PATCH and pass partial=True if it is.
        """
        ser_book = BookSerializer(book, data=request.data, partial=request.method == 'PATCH')

        if ser_book.is_valid():
            ser_book.save()
            return Response(data=ser_book.data, status=status.HTTP_200_OK)
        return Response(ser_book.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def authors_list_view(request) -> Response:
    if request.method == 'GET':
        book_name = request.query_params.get('book_name')

        if book_name:
            authors = Author.objects.filter(author_of_books__title__icontains=book_name).distinct()
        else:
            authors = Author.objects.all()

        ser_authors = AuthorSerializer(authors, many=True)
        return Response(data=ser_authors.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        ser_author = AuthorSerializer(data=request.data)
        if ser_author.is_valid():
            ser_author.save()
            return Response(data=ser_author.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def authors_detail_view(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    ser_author = AuthorSerializer(author, data=request.data, partial=request.method == 'PATCH')

    if ser_author.is_valid():
        ser_author.save()
        return Response(data=ser_author.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def author_books_view(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    author_data = {
        'id': author.id,
        'name': author.name,
        'age': author.age,
        'books': author.get_id_of_books(),
    }

    return Response(author_data)