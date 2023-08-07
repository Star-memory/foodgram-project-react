from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
USER = 'user'
ROLES_CHOICES = [
    (ADMIN, 'Administrator'),
    (USER, 'User'),
]


class User(AbstractUser):

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ['id']

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN or self.is_staff
