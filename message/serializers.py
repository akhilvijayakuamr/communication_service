from rest_framework import serializers
from .models import Message


# Message serializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'user', 'content', 'timestamp', 'read']
        

# Notification serializer

class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    another_user = serializers.IntegerField()
    follower = serializers.IntegerField(required=False)
    post = serializers.IntegerField(required=False)
    content = serializers.CharField(max_length = 20)
    timestamp = serializers.DateTimeField()
    read = serializers.BooleanField()