from rest_framework import filters


class IsAuthorFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(author__isnull=False)


class AuthorBooksByAgeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        author_age = request.query_params.get('author_age')

        if author_age:
            try:
                author_age = int(author_age)
            except ValueError:
                return queryset.none()

            return queryset.filter(author__age__gte=author_age)

        return queryset