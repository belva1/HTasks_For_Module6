from rest_framework import filters


class BookNameFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        book_name = request.query_params.get('book_name')
        if book_name:
            queryset = queryset.filter(author_of_books__title__icontains=book_name)
        return queryset