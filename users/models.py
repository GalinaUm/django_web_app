from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    avatar = models.ImageField(upload_to='users/avatars/%Y/%m', verbose_name='Аватар', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name='Токен подтверждения', blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


