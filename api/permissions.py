from rest_framework import permissions


class AnonymousPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )


class AnonWithCookie(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.session.test_cookie_worked()
            and request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )
