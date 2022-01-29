import os
from io import BytesIO

import requests
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile


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
    point = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]\
        .split(" ")

    data["longitude"] = point[0]
    data["latitude"] = point[1]

    address = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
        "metaDataProperty"]["GeocoderMetaData"]["text"]

    data["address"] = address
    data["coordinates"] = f"{point[1]}, {point[0]}"

    return data
