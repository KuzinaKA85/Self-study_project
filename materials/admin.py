from django.contrib import admin
from materials.models import Course, Section, Lesson


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
