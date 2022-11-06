from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from mixins.models import (
    TimeStampMixin,
    IsActiveMixin,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(
    AbstractBaseUser,
    PermissionsMixin,
    TimeStampMixin,
    IsActiveMixin,
):
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='First Name',
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Last Name',
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='Email',
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='Phone'
    )
    newsletter = models.BooleanField(
        default=False,
        verbose_name='Newsletter'
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is Staff',
        help_text='Is Staff'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Is Superuser',
        help_text='Is Superuser'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
