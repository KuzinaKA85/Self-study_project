from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwner, IsOwnerOrAdmin, IsStudentOrReadOnly, IsTeacher

from .models import Course, Lesson, Section, Test, TestAttempt
from .serializers import CourseSerializer, LessonSerializer, SectionSerializer, TestSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet-класс для курсов.
    Эндпоинты:
        GET /courses/ - список курсов
        POST /courses/ - создание курса
        GET /courses/{id}/ - детали курса
        PUT /courses/{id}/ - обновление курса
        DELETE /courses/{id}/ - удаление курса
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Назначение прав доступа в зависимости от действия."""

        if self.action == "create":
            return [permissions.IsAuthenticated(), IsTeacher()]
        elif self.action == "destroy":
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated(), IsStudentOrReadOnly()]

    def perform_create(self, serializer):
        """При создании устанавливаем текущего пользователя как owner."""

        serializer.save(owner=self.request.user)


class SectionListAPIView(generics.ListAPIView):
    """Список разделов (с фильтрацией по курсу).
    GET /sections/ - все разделы
    GET /sections/?course={id}/ - разделы конкретного курса
    """

    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Фильтрация разделов по параметру course."""

        course_id = self.request.query_params.get("course")
        if course_id:
            return Section.objects.filter(course_id=course_id)
        return Section.objects.all()


class SectionCreateAPIView(generics.CreateAPIView):
    """Создание раздела (только для преподавателей).
    Эндпоинт:
        POST /materials/sections/create/
    """

    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        """Создаёт раздел с проверкой прав владельца курса."""

        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        if course.owner != self.request.user and not self.request.user.is_admin_user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Вы не являетесь владельцем этого курса")

        serializer.save(course=course)


class SectionRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотр раздела.
    Эндпоинт:
        GET /materials/sections/{id}/
    """

    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class SectionUpdateAPIView(generics.UpdateAPIView):
    """Обновление раздела (владелец или администратор).
    Эндпоинты:
        PUT    /materials/sections/update/{id}/  - полное обновление
        PATCH  /materials/sections/update/{id}/  - частичное обновление
    """

    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        """Выполняет обновление раздела с логированием действия."""

        print(f"Раздел {serializer.instance.id} обновлён пользователем {self.request.user}")
        serializer.save()


class SectionDestroyAPIView(generics.DestroyAPIView):
    """Удаление раздела (только для владельца курса или администратора).
    Эндпоинт:
        DELETE /materials/sections/delete/{id}/
    """

    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class LessonListAPIView(generics.ListAPIView):
    """Список уроков (с фильтрацией по разделу).
    Эндпоинты:
        GET /materials/lessons/                 - все уроки
        GET /materials/lessons/?section={id}/    - уроки конкретного раздела
    """

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Фильтрует уроки по параметру section."""

        section_id = self.request.query_params.get("section")
        if section_id:
            return Lesson.objects.filter(section_id=section_id)
        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотр урока.
    Эндпоинт:
        GET /materials/lessons/{id}/
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsStudentOrReadOnly]


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока (только для преподавателей).
    Эндпоинт:
        POST /materials/lessons/create/
    """

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        """Создаёт урок с проверкой прав владельца курса."""

        section_id = self.request.data.get("section")
        section = get_object_or_404(Section, id=section_id)

        if section.course.owner != self.request.user and not self.request.user.is_admin_user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Вы не являетесь владельцем этого курса")

        serializer.save(owner=self.request.user, section=section)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновление урока (владелец или администратор).
    Эндпоинты:
        PUT    /materials/lessons/update/{id}/  - полное обновление
        PATCH  /materials/lessons/update/{id}/  - частичное обновление
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока.
    Эндпоинт:
        DELETE /materials/lessons/delete/{id}/
    """

    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class TestViewSet(ModelViewSet):
    """ViewSet для управления тестами.
    Эндпоинты:
        GET    /materials/tests/           - список всех тестов
        POST   /materials/tests/           - создание теста
        GET    /materials/tests/{id}/      - просмотр теста
        PUT    /materials/tests/{id}/      - полное обновление теста
        PATCH  /materials/tests/{id}/      - частичное обновление теста
        DELETE /materials/tests/{id}/      - удаление теста
    """

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["lesson"]

    def get_permissions(self):
        """Назначение прав доступа в зависимости от действия."""

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """При создании проверяем, что пользователь — владелец урока."""

        lesson_id = self.request.data.get("lesson")
        lesson = get_object_or_404(Lesson, id=lesson_id)

        if lesson.owner != self.request.user and not self.request.user.is_admin_user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Вы не являетесь владельцем этого урока")

        serializer.save()


class CheckTestAPIView(APIView):
    """
    Проверка ответа на тест (отдельный запрос).
    Эндпоинт:
        POST /materials/check-test/
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос на проверку ответа."""

        # Берем данные из запроса
        test_id = request.data.get("test_id")
        user_answer = request.data.get("answer", "").strip()

        # Проверяем, существует ли тест
        if not test_id:
            return Response({"error": "Не указан test_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Тест не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Сравниваем ответы (без учёта регистра и пробелов)
        is_correct = user_answer.lower() == test.correct_answer.strip().lower()

        # Сохраняем попытку
        TestAttempt.objects.create(
            student=request.user,
            test=test,
            user_answer=user_answer,
            is_correct=is_correct
        )

        # Возвращаем результат
        return Response({
            "correct": is_correct,
            "message": "Правильно!" if is_correct else "Неправильно"
        })
