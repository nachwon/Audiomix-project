from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import generics, exceptions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from direct_messages.models import Message
from direct_messages.serializers import InboxSerializer, MessageSerializer, SentSerializer

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
    serializer_class = InboxSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.NotAuthenticated
        return user.received_msgs.filter(inbox_deleted=False)


class InboxDetail(generics.RetrieveDestroyAPIView):
    serializer_class = InboxSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.NotAuthenticated
        return user.received_msgs.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read_date = timezone.now()
        instance.save()
        if instance.inbox_deleted:
            data = {
                "detail": "받은 메세지함에서 삭제된 메세지 입니다."
            }
            raise exceptions.NotFound(data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            "detail": "받은 메세지함에서 메세지가 삭제 되었습니다."
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        if instance.sent_deleted:
            instance.delete()
        else:
            instance.inbox_deleted = True
            instance.save()


class Sent(generics.ListAPIView):
    serializer_class = SentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.NotAuthenticated
        return user.sent_msgs.filter(sent_deleted=False)


class SentDetail(generics.RetrieveDestroyAPIView):
    serializer_class = InboxSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.NotAuthenticated
        return user.sent_msgs.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sent_deleted:
            data = {
                "detail": "보낸 메세지함에서 삭제된 메세지 입니다."
            }
            raise exceptions.NotFound(data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            "detail": "보낸 메세지함에서 메세지가 삭제 되었습니다."
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        if instance.inbox_deleted:
            instance.delete()
        else:
            instance.sent_deleted = True
            instance.save()
