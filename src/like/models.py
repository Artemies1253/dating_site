from django.db import models
from src.user.models import User


class Like(models.Model):
    owner_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="from_like")
    liked_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="liked_user")
