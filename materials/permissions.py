"""
Кастомные права доступа.

В соответствии с заданием:
- Администратор: полный доступ
- Преподаватель: управление своими курсами/уроками
- Студент: только просмотр
"""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права только для администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_user


class IsTeacher(permissions.BasePermission):
    """Права только для преподавателя."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher


class IsOwner(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем объекта."""

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Получаем владельца объекта
        if hasattr(obj, "owner"):
            owner = obj.owner
        elif hasattr(obj, "course") and hasattr(obj.course, "owner"):
            owner = obj.course.owner
        elif hasattr(obj, "section") and hasattr(obj.section, "course"):
            owner = obj.section.course.owner
        else:
            return False

        return owner == user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Доступ для владельца объекта ИЛИ администратора.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin_user:
            return True
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        if hasattr(obj, "course"):
            return obj.course.owner == request.user
        if hasattr(obj, "section"):
            return obj.section.course.owner == request.user
        return False


class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Студенты могут только читать.
    Преподаватели и администраторы могут изменять.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
                request.user.is_teacher or request.user.is_admin_user
        )