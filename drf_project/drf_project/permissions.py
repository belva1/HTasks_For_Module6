from rest_framework import permissions


class IsAdminCreateOrAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated)