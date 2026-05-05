from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    SectionListAPIView,
    SectionCreateAPIView,
    SectionUpdateAPIView,
    SectionDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    SectionRetrieveAPIView,
    CheckTestAPIView,
    TestViewSet,
)

app_name = "materials"

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"tests", TestViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("sections/", SectionListAPIView.as_view(), name="section-list"),
    path("sections/<int:pk>/", SectionRetrieveAPIView.as_view(), name="section-detail"),
    path("sections/create/", SectionCreateAPIView.as_view(), name="section-create"),
    path("sections/update/<int:pk>/", SectionUpdateAPIView.as_view(), name="section-update"),
    path("sections/delete/<int:pk>/", SectionDestroyAPIView.as_view(), name="section-delete"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
    path("check-test/", CheckTestAPIView.as_view(), name="check-test"),
]
