from rest_framework import serializers
from sent_messages.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message_id', 'examinee_id', 'exam_id', 'module_name', 'alert', 'description', 'content', 'created_at')