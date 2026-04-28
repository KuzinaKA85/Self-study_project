from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone_number",
        "country",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "role",
        "country",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "phone_number", "country")
