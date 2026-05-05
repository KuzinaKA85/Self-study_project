"""
Кастомные права доступа.

В соответствии с заданием:
- Администратор: полный доступ
- Преподаватель: управление своими курсами/уроками, тестами
- Студент: только просмотр материалов и прохождение тестов
"""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права только для администратора."""

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""

        return request.user.is_authenticated and request.user.is_admin_user


class IsTeacher(permissions.BasePermission):
    """Права только для преподавателя."""

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""

        return request.user.is_authenticated and request.user.is_teacher


class IsOwner(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем объекта (Course, Section, Lesson, Test, TestAttempt)."""

    def _get_owner(self, obj):
        """Рекурсивно получаем владельца объекта."""

        if hasattr(obj, "owner"):
            return obj.owner
        if hasattr(obj, "course"):
            return self._get_owner(obj.course)
        if hasattr(obj, "section"):
            return self._get_owner(obj.section)
        if hasattr(obj, "lesson"):
            return self._get_owner(obj.lesson)
        if hasattr(obj, "test"):
            return self._get_owner(obj.test)
        return None

    def has_object_permission(self, request, view, obj):
        """Проверка прав на уровне объекта."""

        owner = self._get_owner(obj)
        return owner is not None and owner == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Доступ для владельца объекта ИЛИ администратора.
    """

    def has_object_permission(self, request, view, obj):
        """Проверка прав на уровне объекта."""

        if request.user.is_admin_user:
            return True

        if hasattr(obj, "lesson"):
            return obj.lesson.owner == request.user
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
        """Проверка прав на уровне запроса."""

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (request.user.is_teacher or request.user.is_admin_user)
