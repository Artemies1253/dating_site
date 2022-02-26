import os
from io import BytesIO

import requests
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.core.mail import EmailMessage
from loguru import logger


DELTA_LONGITUDE_1KM = 0.016
DELTA_LATITUDE_1KM = 0.009


def get_path_upload_avatar(instanse, file):
    """Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg"""
    return f"avatar/{instanse.id}/{file}"


def get_avatar_with_water_mark(image) -> InMemoryUploadedFile:
    avatar = Image.open(image)
    avatar_width, avatar_height = avatar.size

    watermark = Image.open(os.path.join(settings.MEDIA_ROOT, os.path.normpath("service_file/water_mark.png")))
    correct_size_watermark = watermark.resize((int(avatar_width / 5), int(avatar_height / 5)))

    transparent = Image.new('RGB', avatar.size, (0, 0, 0, 0))
    transparent.paste(avatar, (0, 0))
    transparent.paste(
        correct_size_watermark, (int(avatar_width / 1.25), int(avatar_height / 1.25)), mask=correct_size_watermark
    )

    image_file = BytesIO()
    transparent.save(image_file, format="png")

    avatar_with_water_mark = SimpleUploadedFile(
        name=image.name, content=image_file.getvalue(), content_type="image/jpeg"
    )
    return avatar_with_water_mark


def get_mutual_sympathy_text(user_from_like):
    text = f"Вы понравились {user_from_like.first_name} {user_from_like.last_name}! {user_from_like.email}. " \
           f"Напишите ему."
    return text


def get_data_address(address: str) -> dict:
    data = {}
    response = requests.get(url=f"https://geocode-maps.yandex.ru/1.x/?apikey={settings.API_YANDEX_KEY}&"
                                f"format=json&geocode={address}")
    point = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"] \
        .split(" ")

    data["longitude"] = point[0]
    data["latitude"] = point[1]

    address = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
        "metaDataProperty"]["GeocoderMetaData"]["text"]

    data["address"] = address

    return data


def get_border_coordinates(longitude, latitude, distance):
    delta_longitude = DELTA_LONGITUDE_1KM * distance
    delta_latitude = DELTA_LATITUDE_1KM * distance
    max_longitude = longitude + delta_longitude
    min_longitude = longitude - delta_longitude
    max_latitude = latitude + delta_latitude
    min_latitude = latitude - delta_latitude

    return {
        'max_longitude': max_longitude,
        'min_longitude': min_longitude,
        'max_latitude': max_latitude,
        'min_latitude': min_latitude
    }


def send_email(subject: str, body: str, email: str):
    logger.add(f"{os.path.dirname(__file__)}/logs/email_exception.log", format="{time} {level} {message}",
               level="ERROR", rotation="4 MB", compression="zip",
               encoding="utf-8")
    logger.add(f"{os.path.dirname(__file__)}/logs/info.log", format="{time} {level} {message}",
               level="INFO", rotation="4 MB", compression="zip",
               encoding="utf-8")
    message = EmailMessage(
        subject=subject,
        body=body,
        to=(email,))
    try:
        message.send()
        logger.info(f"Тема сообщения: {subject} \n"
                    f"Текст: {body}"
                    f"Отправлено {email}"
                    )
    except Exception as ex:
        logger.exception(ex)
        logger.error(f"Ошибка {str(ex)}"
                     f"Тема сообщения: {subject} \n"
                     f"Текст: {body}"
                     f"Отправлено {email}"
                     )


def create_notification(instance, user):
    from src.notification.models import Notification

    if instance.__class__.__name__ == 'Message':
        Notification.objects.create(message=instance, user=user)
    elif instance.__class__.__name__ == 'Like':
        Notification.objects.create(like=instance, user=user)
