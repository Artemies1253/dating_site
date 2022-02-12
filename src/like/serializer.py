from rest_framework import serializers
from rest_framework.serializers import ValidationError

from src.like.models import Like
from src.user.models import User


class CreateLikeSerializer(serializers.Serializer):
    from_like_user_id = serializers.IntegerField()
    liked_user_id = serializers.IntegerField()

    def validate_liked_user_id(self, value):
        if not User.objects.filter(id=value, is_delete=False).exists():
            raise ValidationError("Юзер с таким id не найден")
        return value

    def validate_from_like_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise ValidationError("Юзер с таким id не найден")
        return value

    def save(self, **kwargs):
        from_like_user_id = self.validated_data.get("from_like_user_id")
        liked_user_id = self.validated_data.get("liked_user_id")
        from_like_user = User.objects.get(id=from_like_user_id)
        liked_user = User.objects.get(id=liked_user_id)

        like = Like.objects.get_or_create(owner_user=from_like_user, liked_user=liked_user)

        return like


class LikeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
