from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework import generics, status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from direct_messages.models import Message
from direct_messages.serializers import MessageSerializer

User = get_user_model()


class SendMessage(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        request = serializer.context.get('request')
        serializer.save(from_user=request.user)


class Inbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.NotAuthenticated
        return user.received_msgs.all()


class Sent(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.NotAuthenticated
        return user.sent_msgs.all()
