from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    """Модель пользователя с ролями: Администратор, Преподаватель, Студент"""

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Укажите почту"
    )

    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватарку",
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Введите страну проживания",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Роли по заданию
    ROLE_CHOICES = [
        ("student", "Студент"),
        ("teacher", "Преподаватель"),
        ("admin", "Администратор"),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
        verbose_name="Роль"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    # Вспомогательные свойства
    @property
    def is_teacher(self):
        """Проверка, является ли пользователь преподавателем"""

        return self.role == "teacher" or self.is_staff

    @property
    def is_student(self):
        """Проверка, является ли пользователь студентом"""

        return self.role == "student"

    @property
    def is_admin_user(self):
        """Проверка, является ли пользователь администратором"""

        return self.is_staff or self.is_superuser or self.role == "admin"