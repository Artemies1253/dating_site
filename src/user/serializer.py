import datetime

from rest_framework import serializers

from src.user.models import User, Ava, UserImage


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "gender", "avatar")


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ava
        fields = ("photo", "is_active")

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

