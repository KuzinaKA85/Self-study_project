from django.core.validators import FileExtensionValidator
from django.db import models

from config import settings


class Course(models.Model):
    """Модель курса."""

    title_course = models.CharField(
        max_length=250,
        verbose_name="Наименование курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/",
        verbose_name="Превью курса",
        help_text="Загрузите изображение для превью курса",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
    )
    description = models.TextField(verbose_name="Описание курса", help_text="Введите подробное описание курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован",
        help_text="Отметьте, если курс доступен для просмотра",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец (преподаватель)",
        related_name="courses",
        null=True,
        blank=True,
        help_text="Укажите владельца курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title_course


class Section(models.Model):
    """Модель для раздела курса."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections", verbose_name="Курс")
    title_section = models.CharField(max_length=200, verbose_name="Название раздела")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядковый номер раздела")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["order"]

    def __str__(self):
        """Строковое представление раздела."""

        return f"{self.course.title_course} — {self.title_section}"


class Lesson(models.Model):
    """Модель урока."""

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Раздел",
        help_text="Выберите раздел курса, к которому относится урок",
    )
    title_lesson = models.CharField(
        max_length=250,
        verbose_name="Наименование урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Введите подробное описание урока",
        blank=True,
    )
    preview = models.ImageField(
        upload_to="lessons/",
        verbose_name="Превью урока",
        help_text="Загрузите изображение для превью урока",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", help_text="Вставьте ссылку на видео", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    order = models.PositiveIntegerField(default=0, verbose_name="Порядковый номер урока")

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="lessons",
        null=True,
        blank=True,
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["order", "created_at"]

    def __str__(self):
        """Строковое представление урока."""

        return f"{self.section.title_section} - {self.title_lesson}"


class Test(models.Model):
    """Модель теста для урока."""

    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="test", verbose_name="Урок")
    question = models.TextField(verbose_name="Вопрос")
    correct_answer = models.CharField(max_length=800, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        """Строковое представление теста."""

        return f"Тест: {self.lesson.title_lesson}"


class TestAttempt(models.Model):
    """Модель для попытки прохождения теста."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_attempts", verbose_name="Студент"
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts", verbose_name="Тест")
    user_answer = models.CharField(max_length=800, verbose_name="Ответ студента")
    is_correct = models.BooleanField(default=False, verbose_name="Правильно?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def save(self, *args, **kwargs):
        """При сохранении автоматически проверяем ответ."""

        user_ans = self.user_answer.strip().lower()
        correct_ans = self.test.correct_answer.strip().lower()
        self.is_correct = user_ans == correct_ans
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Попытка теста"
        verbose_name_plural = "Попытки тестов"
        ordering = ["-created_at"]

    def __str__(self):
        """Строковое представление попытки теста."""

        return (
            f"{self.student.email} — {self.test.lesson.title_lesson} — "
            f"{'Правильно!' if self.is_correct else 'Неправильно!'}"
        )
