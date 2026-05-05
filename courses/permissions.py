# courses/permissions.py
from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True

        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Только администраторы могут изменять объекты
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return request.user and request.user.is_staff


class CanCreateCoursePermission(permissions.BasePermission):
    """
    Проверка прав на создание курса
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CanDeleteLessonPermission(permissions.BasePermission):
    """
    Проверка прав на удаление урока
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True
        return obj.author == request.user

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user