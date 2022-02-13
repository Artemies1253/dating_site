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

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class Ava(models.Model):
    photo = models.ImageField(default='/media/avatar/default_avatar.jpg',
                              upload_to=get_path_upload_avatar,
                              validators=[FileExtensionValidator(allowed_extensions=["jpg"])])
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='ava')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)


class UserImage(models.Model):
    image = models.ImageField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='image')
    created_at = models.DateTimeField(auto_now_add=True)
