import os
from io import BytesIO

import requests
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile


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
    point = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]\
        .split(" ")

    data["longitude"] = point[0]
    data["latitude"] = point[1]

    address = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
        "metaDataProperty"]["GeocoderMetaData"]["text"]

    data["address"] = address

    return data

def get_nearest_users(user, distance):
    from src.user.models import User
    longitude = user.longitute
    latitude = user.latitude
    delta_longitude = DELTA_LONGITUDE_1KM * distance
    delta_latitude = DELTA_LATITUDE_1KM * distance
    nearest_users_queryset = User.object.filter(longitude__lte=longitude+delta_longitude)\
                                            .exclude(longitude__lt=longitude-delta_longitude)\
                                            .exclude(latitude__gt=latitude+delta_latitude)\
                                            .exclude(latitude__lt=latitude-delta_latitude)\
                                            .exclude(id=user.id)
    return nearest_users_queryset   

                                         
# long = User.objects.get('longitude')
# long = User.objects.filter('logitude' lt 'longitude+0.16' and 'logitude' gt 'longtude-0.16' )

# def get_user_coordinates(user_id):
#     user = User.objects.filter(id=user_id)
#     longitude = user.longitute
#     latitude = user.latitude
#     return longitude, latitude

# def nearest_users():
    