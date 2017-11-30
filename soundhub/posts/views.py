from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Post, CommentTrack
from posts.serializers import PostSerializer, CommentTrackSerializer

from utils.permissions import IsAuthorOrReadOnly


# 포스트 목록 조회 및 포스트 생성 API
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        # 회원인 경우만 포스트 작성 가능
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 단일 포스트 조회, 수정, 삭제 API
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        # 작성자인 경우만 포스트 수정, 삭제 가능
        IsAuthorOrReadOnly,
    )


# 코멘트 트랙 조회, 등록
class CommentTrackList(generics.ListCreateAPIView):
    serializer_class = CommentTrackSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    # 쿼리셋 가져오기
    def get_queryset(self):
        # GET 요청인 경우 코멘트 트랙 리스트 가져옴
        if self.request.method == 'GET':
            pk = self.kwargs['pk']
            post = Post.objects.get(pk=pk)
            return post.comment_tracks.all()
        # POST 요청인 경우 pk 값으로 포스트 객체 가져옴
        elif self.request.method == 'POST':
            return Post.objects.all()

    # POST 요청 받을 시
    def perform_create(self, serializer):
        post = self.get_object()
        serializer.save(
            # 요청 보낸 유저를 코멘트 작성자로
            author=self.request.user,
            # pk 값으로 가져온 포스트 객체에 코멘트 작성
            post=post,
        )


class CommentTrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentTrack.objects.all()
    serializer_class = CommentTrackSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )
