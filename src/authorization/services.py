from datetime import timedelta, datetime
import jwt
from django.conf import settings
from django.urls import reverse

from src.base.services import send_email
from src.user.models import User


def create_token(user_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "user_id": user_id,
        "access_token": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "Token"
    }


def create_access_token(data: dict, expires_delta: timedelta = 15):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "sub": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGOTITHM)
    return encoded_jwt


def send_registration_email(user):
    token = create_token(user.id).get("access_token")
    domain = settings.HOST
    link = str(domain) + str(reverse(viewname="verify_email", kwargs={"token": token}))
    body = f"Ваш email был указан при регистрации на сайте Dating Site," \
           f"Если это были не вы, просто проигнорируйте данное сообщение" \
           f"Для окончания регистрации вам не обходимо перейти по ссылке ниже \n" \
           f"{link}\n" \
           f"Пожалуйста, не отвечайте на данное письмо, оно сгенерировано автоматически."
    send_email(subject="Подтверждение регистрации", body=body, email=user.email)


def send_email_of_success_registration(user):
    body = f"Вы успешно зарегистрировались на сайте Dating Site.\n" \
           f"Желаем побыстрее найти новые знакомства\n" \
           f"Пожалуйста, не отвечайте на данное письмо, оно сгенерировано автоматически."
    send_email(subject="Успешная регистрация", body=body, email=user.email)


def verify_user_email_by_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGOTITHM)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_verified:
        user.is_verified = True
        user.save()

    send_email_of_success_registration(user)
