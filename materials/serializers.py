from rest_framework import serializers
from .models import Course, Section, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course."""

    owner_email = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["owner", "created_at"]


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Section."""

    class Meta:
        model = Section
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson."""

    owner_email = serializers.ReadOnlyField(source="owner.email")
    section_title = serializers.ReadOnlyField(source="section.title_section")
    course_title = serializers.ReadOnlyField(source="section.course.title_course")

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["owner", "created_at"]
