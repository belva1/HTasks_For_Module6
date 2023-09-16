from rest_framework import filters


class IsAuthorFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(author__isnull=False)
