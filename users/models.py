from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True"))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(
        max_length=128,
        verbose_name=_("Username")
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email")
    )
    full_name = models.CharField(
        max_length=128,
        verbose_name=_("Full name")
    )
    phone_number = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Phone number")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active")
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Is staff")
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = _("User")
        verbose_name_plural = _("Users")
