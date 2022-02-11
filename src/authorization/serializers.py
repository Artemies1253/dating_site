from rest_framework import serializers

from src.base.services import get_avatar_with_water_mark, get_data_address
from src.user.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, max_length=30)
    password_repeat = serializers.CharField(min_length=4, max_length=30)

    def validate(self, values):
        password = values.get("password")
        password_repeat = values.get("password_repeat")
        if password == password_repeat:
            return values
        else:
            raise serializers.ValidationError("Пароли не совпадают")

    def create(self, validated_data):
        user = User.object.create_user(email=validated_data.get("email"), password=validated_data.get("password"))
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.gender = validated_data.get("gender")
        raw_address = validated_data.get('address')
        data_address = get_data_address(raw_address)
        if data_address:
            user.longitude = data_address["longitude"]
            user.latitude = data_address["latitude"]
            user.address = data_address["address"]
        avatar = validated_data.get("avatar")
        avatar_with_water_mark = get_avatar_with_water_mark(avatar)
        user.avatar = avatar_with_water_mark
        user.save()
        user = User.object.get(email=validated_data.get("email"))
        return user

    class Meta:
        model = User
        exclude = ("is_admin", "latitude", "longitude")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, max_length=30)
