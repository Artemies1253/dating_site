from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import get_path_upload_avatar


class User(models.Model):
    GENDER_CHOICES = (
        ("m", "man"),
        ("w", "woman")
    )
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg"])]
    )
    is_staff = models.BooleanField(default=False, blank=True)
    is_super_user = models.BooleanField(default=False, blank=True)

    @property
    def is_authenticated(self):
        """Всегда возвращает True. Это способ узнать, был ли пользователь аутентифицирован"""

        return True

    def __str__(self):
        return self.email
