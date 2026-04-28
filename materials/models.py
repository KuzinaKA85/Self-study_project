from django.core.validators import FileExtensionValidator
from django.db import models


class Course(models.Model):
    """Модель курса"""

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
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите подробное описание курса"
    )
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
    """Модель для раздела курса"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name="Курс"
    )
    title_section = models.CharField(max_length=200, verbose_name="Название раздела")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title_course} — {self.title_section}"


class Lesson(models.Model):
    """Модель урока"""

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
    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="Вставьте ссылку на видео", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок урока")

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
        return f"{self.section.title_section} - {self.title_lesson}"

