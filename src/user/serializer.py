import datetime

from rest_framework import serializers

from src.base.services import get_data_address, get_avatar_with_water_mark
from src.user.models import User, Ava, UserImage


class UserDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "status_text", "gender", "avatar")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "email", "is_admin", "is_delete", "password", "is_superuser",
            "user_permissions", "last_login", "address", "latitude", "longitude"
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "is_admin", "is_delete", "password", "is_superuser",
            "user_permissions", "last_login", "latitude", "longitude",
        )

    def validate_address(self, value):
        data_address = get_data_address(value)
        if not data_address:
            serializers.ValidationError("Не корректный адреc")
        return data_address

    def update(self, instance, validated_data):
        avatar = validated_data.get("avatar")
        if avatar:
            instance.avatar = get_avatar_with_water_mark(avatar)
        data_address = validated_data.get("address")
        if data_address:
            instance["address"] = data_address["address"]
            instance["longitude"] = data_address["longitude"]
            instance["latitude"] = data_address["latitude"]
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.hobby = validated_data.get("hobby", instance.hobby)
        instance.about_myself = validated_data.get("about_myself", instance.about_myself)
        instance.status_text = validated_data.get("status_text", instance.status_text)
        instance.favorite_quotes = validated_data.get("favorite_quotes", instance.favorite_quotes)
        instance.purpose_relationship = validated_data.get("purpose_relationship", instance.purpose_relationship)

        instance.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("is_admin", "is_delete", "password", "is_superuser", "user_permissions", "last_login")


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ava
        fields = ("photo",)

    def create(self, validated_data):
        user = validated_data['user']
        current_avatar = Ava.objects.get(is_active=True, user=user)
        new_avatar = Ava(**validated_data)
        new_avatar.save()
        current_avatar.is_active = False
        current_avatar.save()

        return Ava(**validated_data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ("image",)

