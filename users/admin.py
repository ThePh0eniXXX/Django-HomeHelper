from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserGroup, GroupMembership
from django.utils.html import format_html

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'created_at', 'invitation_link')
    readonly_fields = ('invitation_code', 'invitation_link',)
    inlines = [GroupMembershipInline]

    def invitation_link(self, obj):
        # Получаем полную ссылку через метод get_invitation_url() вашей модели
        url = obj.get_invitation_url() if hasattr(obj, 'get_invitation_url') else ''
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.invitation_code)
    invitation_link.short_description = 'Invitation Link'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Дополнительная информация', {
            'fields': (
                'phone', 'birth_date', 'avatar',
                'language_preference', 'timezone', 'country', 'preferred_currency',
                'is_beta_tester', 'external_id', 'provider',
                'receive_reminders', 'reminder_time', 'dark_mode_enabled',
            )
        }),
        ('Группы', {
            'fields': ('group_list',),
            'classes': ('collapse',)  # делает секцию сворачиваемой
        }),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('group_list',)
    filter_horizontal = ('user_permissions',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'country', 'preferred_currency', 'is_beta_tester', 'group_list')
    search_fields = ("email", "username", "first_name", "last_name")

    def group_list(self, obj):
        groups = obj.membership_groups.all()
        if groups:
            # Если групп много, можно вывести, например, только количество и первые несколько
            group_names = [group.name for group in groups]
            if len(group_names) > 5:
                return ", ".join(group_names[:5]) + f", ... ({len(group_names)} total)"
            return ", ".join(group_names)
        return "Нет групп"
    group_list.short_description = 'Groups'

