from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        '''Разрешаем только безопасные методы.'''
        return request.method in SAFE_METHODS or  request.user.is_staff
