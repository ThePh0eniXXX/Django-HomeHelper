from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import UserGroup, GroupMembership

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['id', 'name', 'description', 'group_type', 'invitation_code', 'created_at', 'updated_at']


class GroupMembershipSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'group', 'role', 'joined_at']


def validate_invitation_code(value):
    try:
        UserGroup.objects.get(invitation_code=value)
    except UserGroup.DoesNotExist:
        raise serializers.ValidationError("Invalid invitation code.")
    return value


class GroupJoinSerializer(serializers.Serializer):
    invitation_code = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    # Можно добавить поле, отображающее участие в группах, если нужно:
    group_memberships = GroupMembershipSerializer(many=True, read_only=True, source='group_memberships')

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name",
            "phone", "birth_date", "avatar",
            # удаляем family_group
            "role_in_family",  # можно оставить, если планируете использовать параллельно с новой системой
            "language_preference", "timezone", "country", "preferred_currency",
            "is_beta_tester", "external_id", "provider",
            "receive_reminders", "reminder_time", "dark_mode_enabled",
            "date_joined", "last_login", "is_active", "is_staff",
            "group_memberships"  # новое поле для отображения групп
        ]
        read_only_fields = ("id", "email", "username", "date_joined", "last_login", "is_staff", "is_active", "external_id", "provider")
