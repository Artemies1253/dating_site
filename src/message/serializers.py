from rest_framework import serializers

from src.message.models import Message


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'receiver')


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageUpdateOrDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text',)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text')
        instance.is_updated = True
        instance.save()
        return instance
