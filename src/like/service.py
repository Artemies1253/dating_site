from django.core import mail
from django.core.mail import EmailMessage

from src.like.models import Like
from src.user.models import User
from src.base.services import get_mutual_sympathy_text


def is_mutual_like(user_1: User, user_2: User):
    like_1 = Like.objects.filter(owner_user=user_1, liked_user=user_2)
    like_2 = Like.objects.filter(owner_user=user_2, liked_user=user_1)
    if like_1.exists() and like_2.exists():
        return True


def send_email_of_like(user_1: User, user_2: User):
    email_1 = EmailMessage(
        subject="У вас взаимная симпатия",
        body=get_mutual_sympathy_text(user_2),
        to=(user_1.email,)
    )
    email_2 = EmailMessage(
        subject="У вас взаимная симпатия",
        body=get_mutual_sympathy_text(user_1),
        to=(user_2.email,)
    )
    # connection = mail.get_connection()
    # connection.send_messages((email_1, email_2))
