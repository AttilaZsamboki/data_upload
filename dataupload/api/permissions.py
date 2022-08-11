from rest_framework import permissions


class AuthorAllUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.COOKIES['id.6nz455rn']:
            return True
