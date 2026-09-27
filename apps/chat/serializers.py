from rest_framework import serializers

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "role",
            "content",
            "created_at",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "created_at",
            "messages",
        ]


class ChatMessageSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField()
    message = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class RegenerateMessageSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField()
    message_id = serializers.IntegerField()


class RenameConversationSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=120,
        allow_blank=False,
        trim_whitespace=True,
    )