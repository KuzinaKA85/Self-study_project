from django.contrib import admin
from materials.models import Course, Section, Lesson, Test, TestAttempt


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title_course",
        "description",
        "created_at",
        "is_published",
        "owner",
    )
    search_fields = ("title_course", "owner__email")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "title_section",
        "order",
    )
    search_fields = ("title_section", "course__title_course")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "section",
        "title_lesson",
        "description",
        "video_url",
        "created_at",
        "owner",
    )
    list_filter = ("section", "created_at", "owner")
    search_fields = ("title_lesson", "section", "owner")


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Админка для модели Test."""

    list_display = ("id", "lesson", "question", "correct_answer")
    list_filter = ("lesson__section__course",)
    search_fields = ("question", "lesson__title_lesson")


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    """Админка для модели TestAttempt."""

    list_display = ("id", "student", "test", "user_answer", "is_correct", "created_at")
    list_filter = ("is_correct", "created_at", "test__lesson__section__course")
    search_fields = ("student__email", "user_answer")
    readonly_fields = ("created_at",)
