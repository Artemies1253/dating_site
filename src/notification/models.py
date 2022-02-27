from django.db import models

from src.like.models import Like
from src.message.models import Message
from src.user.models import User


class Notification(models.Model):
    message = models.ForeignKey(to=Message, null=True, blank=True, on_delete=models.CASCADE)
    like = models.OneToOneField(to=Like, null=True, blank=True, on_delete=models.CASCADE)
    is_unread = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
