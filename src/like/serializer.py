from rest_framework import serializers
from rest_framework.serializers import ValidationError

from src.base.services import create_notification
from src.like.models import Like
from src.like.service import is_mutual_like, send_email_of_like
from src.user.models import User


class CreateLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ("owner_user", "liked_user")

    def validate(self, attrs):
        owner_user = attrs.get("owner_user")
        liked_user = attrs.get("liked_user")
        if Like.objects.filter(owner_user=owner_user, liked_user=liked_user).exists():
            raise ValidationError("Пользователь уже поставил данному пользователю лайк")

        return attrs

    def create(self, validated_data):
        owner_user = validated_data.get("owner_user")
        liked_user = validated_data.get("liked_user")
        like = Like.objects.create(owner_user=owner_user, liked_user=liked_user)
        create_notification(instance=like, user=liked_user)

        return like


class LikeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
