from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """Проверка прав администратора."""
    message = 'Нужны права администратора'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка прав администратора."""
    message = 'Нужны права администратора.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin'
                    or request.user.is_superuser)))


class IsAdminOrModeratirOrAuthor(permissions.BasePermission):
    """"Проверка прав для отзывов и комментариев."""
    message = 'Нужны права администратора/модератора или автора'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or request.user == obj.author
        )
