from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import get_path_upload_avatar
from src.user.user_manager import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ("m", "male"),
        ("f", "female")
    )
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        validators=[FileExtensionValidator(allowed_extensions=["jpg"])]
    )
    is_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=150)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    hobby = models.TextField(max_length=1000, null=True, blank=True)
    about_myself = models.TextField(max_length=3000, null=True, blank=True)
    status_text = models.CharField(max_length=255, null=True, blank=True)
    favorite_quotes = models.TextField(max_length=1000, null=True, blank=True)
    purpose_relationship = models.CharField(max_length=50, null=True, blank=True)
    is_delete = models.BooleanField(default=False, blank=True)
    is_verifired = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
