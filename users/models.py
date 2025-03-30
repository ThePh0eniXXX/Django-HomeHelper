from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
