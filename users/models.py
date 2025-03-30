from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
import pycountry

CURRENCY_CHOICES = sorted(
    [(c.alpha_3, f"{c.alpha_3} - {c.name}") for c in pycountry.currencies],
    key=lambda x: x[0]
)

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
    family_group = models.CharField(max_length=255, blank=True, null=True)
    role_in_family = models.CharField(
        max_length=50,
        choices=[
            ('parent', 'Parent'),
            ('child', 'Child'),
            ('roommate', 'Roommate'),
            ('other', 'Other')
        ],
        blank=True,
        null=True
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
