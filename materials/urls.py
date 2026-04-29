from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    CourseViewSet, SectionListAPIView, SectionCreateAPIView,
    SectionUpdateAPIView, SectionDestroyAPIView,
    LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView,
    LessonUpdateAPIView, LessonDestroyAPIView
)

app_name = "materials"

# Настройка роутера для ViewSet
router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    # ViewSet
    path("", include(router.urls)),

    # Разделы
    path("sections/", SectionListAPIView.as_view(), name="section-list"),
    path("sections/create/", SectionCreateAPIView.as_view(), name="section-create"),
    path("sections/update/<int:pk>/", SectionUpdateAPIView.as_view(), name="section-update"),
    path("sections/delete/<int:pk>/", SectionDestroyAPIView.as_view(), name="section-delete"),

    # Уроки
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
]