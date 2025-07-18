from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)  # CharField example

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'display_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_username = serializers.SerializerMethodField()  # SerializerMethodField example

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_username', 'conversation', 'message_body', 'sent_at', 'is_read']

    def get_sender_username(self, obj):
        return obj.sender.username


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")  # ValidationError example
        return value
