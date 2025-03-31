from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
import pycountry
from django.conf import settings
from django.utils.crypto import get_random_string

CURRENCY_CHOICES = sorted(
    [(c.alpha_3, f"{c.alpha_3} - {c.name}") for c in pycountry.currencies],
    key=lambda x: x[0]
)

GROUP_TYPE_CHOICES = [
    ('family', 'Семья'),
    ('work', 'Коллеги'),
    ('friends', 'Друзья'),
    ('other', 'Другое'),
]

class UserGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    group_type = models.CharField(max_length=50, choices=GROUP_TYPE_CHOICES, blank=True, null=True)
    invitation_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.invitation_code:
            # Генерируем код длиной 32 символа (можно добавить URL-префикс при необходимости)
            self.invitation_code = get_random_string(32)
        super().save(*args, **kwargs)

    def get_invitation_url(self):
        # Предположим, что у вас настроена переменная SITE_URL в settings.py
        from django.urls import reverse
        relative_url = reverse('group-join')
        return f"{self.site_url}{relative_url}?invitation_code={self.invitation_code}"

    @property
    def site_url(self):
        # Пример – добавьте SITE_URL в settings.py, например, http://localhost:8000
        from django.conf import settings
        return getattr(settings, 'SITE_URL', 'http://localhost:8000')

    def __str__(self):
        return self.name


class User(AbstractUser):
    # Основные поля
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Расширенные поля
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    # Контекст домохозяйства

    membership_groups = models.ManyToManyField(
        'UserGroup',
        through='GroupMembership',
        related_name='members',
        blank=True
    )

    # Персонализация
    language_preference = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    country = CountryField(blank=True, null=True)
    preferred_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD'
    )
    dark_mode_enabled = models.BooleanField(default=False)

    # Уведомления
    receive_reminders = models.BooleanField(default=True)
    reminder_time = models.TimeField(blank=True, null=True)

    # OAuth / внешняя авторизация
    external_id = models.CharField(max_length=255, blank=True, null=True)
    provider = models.CharField(
        max_length=50,
        choices=[
            ('google', 'Google'),
            ('yandex', 'Yandex'),
            ('apple', 'Apple'),
            ('vk', 'VK'),
            ('email', 'Email/Password')
        ],
        default='email'
    )

    # Участие в тестировании
    is_beta_tester = models.BooleanField(default=False)

    def __str__(self):
        return self.email or self.username

class GroupMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('member', 'Участник'),
        ('moderator', 'Модератор'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    group = models.ForeignKey(
        UserGroup,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user} в группе {self.group} как {self.role}"