import datetime

from django.db import models

from src.base.services import create_notification
from src.user.models import User


class Like(models.Model):
    owner_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="from_like")
    liked_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="liked_user")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Лайк от пользователя {self.owner_user} - пользователю {self.liked_user}"

    class Meta:
        verbose_name = "Лайк пользователю"
        verbose_name_plural = "Лайки пользователям"
