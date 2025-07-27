from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import PermissionDenied

ADMIN = 'ADMIN'
USER = 'USER'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', USER)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', ADMIN)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    STATUS_CHOICES = [
        (ADMIN, "Администратор"),
        (USER, "Пользователь"),
    ]

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Имя", help_text="Укажите имя")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Фамилия", help_text="Укажите фамилию")
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    role = models.CharField(max_length=13, choices=STATUS_CHOICES, default=USER, verbose_name="Роль пользователя")
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        if self.pk and 'role' in kwargs.get('update_fields', []) or 'role' in self.get_dirty_fields():
            original_user = User.objects.get(pk=self.pk)
            if original_user.role != self.role:
                # Проверяем, есть ли доступ у запрашивающего пользователя
                request = kwargs.pop('request', None)
                if not request or not request.user.is_superuser:
                    raise PermissionDenied("Только администратор может изменять роль")
        super().save(*args, **kwargs)

    def get_dirty_fields(self):
        dirty_fields = {}
        if not self.pk:
            return dirty_fields
        user = User.objects.get(pk=self.pk)
        for field in self._meta.fields:
            field_name = field.name
            original_val = getattr(user, field_name)
            current_val = getattr(self, field_name)
            if original_val != current_val:
                dirty_fields[field_name] = original_val
        return dirty_fields