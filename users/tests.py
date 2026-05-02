from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserRegistrationTests(APITestCase):
    """Тесты для регистрации и профиля пользователя."""

    def setUp(self):
        """Подготовка перед каждым тестом."""

        self.register_url = reverse("users:register")
        self.login_url = reverse("users:login")
        self.profile_url = "/users/profile/"

        # Создаём тестового пользователя
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "phone_number": "+79123456789",
            "first_name": "Test",
            "last_name": "User",
        }
        self.client.post(self.register_url, self.user_data)
        self.user = User.objects.get(email="test@example.com")

    def test_register_user_success(self):
        """Тест: успешная регистрация нового пользователя."""

        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "phone_number": "+79123456789",
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_register_user_invalid_email(self):
        """Тест: регистрация с невалидным email."""

        data = {"email": "not-an-email", "password": "testpass123"}
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_retrieve(self):
        """Тест: Пользователь может войти и получить JWT токен."""

        # Логинимся и получаем токен
        login_response = self.client.post(self.login_url, {"email": "test@example.com", "password": "testpass123"})
        access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Получаем профиль
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_profile_update(self):
        """Тест: Пользователь может обновить свой профиль."""

        # Логинимся и получаем токен
        login_response = self.client.post(self.login_url, {"email": "test@example.com", "password": "testpass123"})
        access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Обновляем профиль (используем PATCH для частичного обновления)
        response = self.client.patch(
            self.profile_url, {"first_name": "Updated", "last_name": "User", "country": "Russia"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные обновились
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.country, "Russia")
