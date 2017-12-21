from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from direct_messages.serializers import MessageSerializer
from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()


class SendMessage(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        return user.sent_msgs.all()

    def perform_create(self, serializer):
        request = serializer.context.get('request')
        serializer.save(from_user=request.user)
