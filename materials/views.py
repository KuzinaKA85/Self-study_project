from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Course, Section, Lesson
from .serializers import (
    CourseSerializer, SectionSerializer, LessonSerializer
)

from materials.permissions import IsTeacher, IsOwner, IsOwnerOrAdmin, IsStudentOrReadOnly


class CourseViewSet(ModelViewSet):
    """ViewSet-класс для курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Назначение прав доступа в зависимости от действия."""
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsTeacher()]
        elif self.action == "destroy":
            return [permissions.IsAuthenticated(), IsOwner()]
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated(), IsStudentOrReadOnly()]

    def perform_create(self, serializer):
        """При создании устанавливаем текущего пользователя как owner."""
        serializer.save(owner=self.request.user)


class SectionListAPIView(generics.ListAPIView):
    """Список разделов (с фильтрацией по курсу)."""

    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get("course")
        if course_id:
            return Section.objects.filter(course_id=course_id)
        return Section.objects.all()


class SectionCreateAPIView(generics.CreateAPIView):
    """Создание раздела (только для преподавателей)."""

    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        if course.owner != self.request.user and not self.request.user.is_admin_user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы не являетесь владельцем этого курса")

        serializer.save(course=course)

class SectionRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотр раздела."""

    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class SectionUpdateAPIView(generics.UpdateAPIView):
    """Обновление раздела (владелец или администратор)."""

    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        """Дополнительная логика при обновлении."""

        print(f"Раздел {serializer.instance.id} обновлён пользователем {self.request.user}")
        serializer.save()


class SectionDestroyAPIView(generics.DestroyAPIView):
    """Удаление раздела (только для владельца курса или администратора)."""
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class LessonListAPIView(generics.ListAPIView):
    """Список уроков (с фильтрацией по разделу)."""

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        section_id = self.request.query_params.get("section")
        if section_id:
            return Lesson.objects.filter(section_id=section_id)
        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотр урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsStudentOrReadOnly]


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока (только для преподавателей)."""

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        section_id = self.request.data.get("section")
        section = get_object_or_404(Section, id=section_id)

        if section.course.owner != self.request.user and not self.request.user.is_admin_user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы не являетесь владельцем этого курса")

        serializer.save(owner=self.request.user, section=section)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновление урока (владелец или администратор)."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока (только владелец)."""

    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
