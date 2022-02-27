from django.db import models

from src.base.services import create_notification
from src.user.models import User


class Message(models.Model):
    text = models.CharField(max_length=2500)
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='author')
    receiver = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return f'Сообщение от {self.author} для {self.receiver}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
