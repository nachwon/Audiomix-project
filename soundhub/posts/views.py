from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Post, CommentTrack
from posts.serializers import PostSerializer, CommentTrackSerializer

from utils.permissions import IsOwnerOrReadOnly


# 포스트 목록 조회 및 포스트 생성 API
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 단일 포스트 조회, 수정, 삭제 API
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )


class CommentTrackList(generics.ListCreateAPIView):
    queryset = CommentTrack.objects.all()
    serializer_class = CommentTrackSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.post,
        )

