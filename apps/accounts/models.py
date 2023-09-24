from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, password, **kwargs):
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create(self, **kwargs):
        return self.create_user(**kwargs)


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    birthdate = models.DateField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.username
