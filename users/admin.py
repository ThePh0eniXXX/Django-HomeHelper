from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительная информация", {
            "fields": (
                "phone", "birth_date", "avatar",
                "family_group", "role_in_family",
                "language_preference", "timezone", "country", "preferred_currency",
                "is_beta_tester", "external_id", "provider",
                "receive_reminders", "reminder_time", "dark_mode_enabled",
            )
        }),
    )

    list_display = (
        "email", "username", "first_name", "last_name",
        "family_group", "role_in_family", "country", "preferred_currency", "is_beta_tester"
    )
    search_fields = ("email", "username", "first_name", "last_name")
