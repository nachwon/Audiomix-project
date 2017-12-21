from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'to_user',
            'from_user',
            'content',
            'created_date'
        )


class InboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'from_user',
            'content',
            'created_date'
        )


class SentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'to_user',
            'content',
            'read_date',
            'created_date'
        )
