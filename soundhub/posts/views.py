from rest_framework import generics

from posts.models import Post


# 포스트 목록 조회 및 포스트 생성 API
from posts.serializers import PostSerializer
from utils.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )
