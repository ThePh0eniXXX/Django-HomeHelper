from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    country = CountryField(required=False)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name",
            "phone", "birth_date", "avatar",
            "family_group", "role_in_family",
            "language_preference", "timezone", "country", "preferred_currency",
            "is_beta_tester", "external_id", "provider",
            "receive_reminders", "reminder_time", "dark_mode_enabled",
            "date_joined", "last_login", "is_active", "is_staff"
        ]
        read_only_fields = ("id", "email", "username", "date_joined", "last_login", "is_staff", "is_active", "external_id", "provider")
