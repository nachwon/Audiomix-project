from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'from_user',
            'to_user',
            'content',
            'sent_date'
        )
