from django.contrib.auth import get_user_model
from rest_framework import generics

from direct_messages.serializers import MessageSerializer
from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()


class SendMessage(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        return user.sent_msgs.all()
