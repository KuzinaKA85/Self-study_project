from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Swagger документация
schema_view = get_schema_view(
    openapi.Info(
        title="SELF-STUDY API",
        default_version="v1",
        description="API для управления образовательными материалами. Позволяет создавать курсы, разделы, уроки и тесты",
        contact=openapi.Contact(email="kuzina_ka@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("materials/", include("materials.urls", namespace="materials")),
    path("users/", include("users.urls", namespace="users")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
