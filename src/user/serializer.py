from rest_framework import serializers

from src.user.models import User


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "gender", "avatar")
