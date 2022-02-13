from rest_framework import serializers

from src.user.models import User, Ava


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "gender", "avatar")


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ava
        fields = ("photo", "is_active")

        # def create(self):
        #     current_avatar = Ava.objects.get(id=self.request.user.id)
        #     print(current_avatar.is_active)
        #     current_avatar.is_active = False

