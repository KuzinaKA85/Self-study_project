from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsAdmin
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    ViewSet для управления пользователями (только для администраторов).
    Эндпоинты:
        GET /users/users/ - список всех пользователей
        POST /users/users/ - создать пользователя
        GET /users/users/{id}/ - детали пользователя
        PUT /users/users/{id}/ - обновить пользователя
        DELETE /users/users/{id}/ - удалить пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)


class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя (студента).
    POST /users/register/
    Тело запроса: {"email": "user@test.ru", "password": "123456"}
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """При создании пользователя устанавливаем роль "student"."""

        serializer.save(role="student")


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и редактирование своего профиля.
    GET /users/profile/ - получить данные своего профиля
    PUT /users/profile/ - обновить данные профиля
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Возвращает текущего аутентифицированного пользователя."""

        return self.request.user
