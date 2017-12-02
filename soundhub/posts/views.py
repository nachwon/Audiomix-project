from rest_framework import generics
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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


# 코멘트 트랙 조회, 등록 API
class CommentTrackList(generics.ListCreateAPIView):
    serializer_class = CommentTrackSerializer
    permission_classes = (
        # 등록된 회원에게만 등록 권한 부여
        IsAuthenticatedOrReadOnly,
    )

    # 쿼리셋 가져오기
    def get_queryset(self):
        # GET 요청인 경우 코멘트 트랙 리스트 가져옴
        if self.request.method == 'GET':
            # URL에서 pk 값을 받아서
            pk = self.kwargs['pk']
            # 필터링을 하여
            post = Post.objects.filter(pk=pk).exists()
            # 해당 pk값을 가진 포스트가 존재하면,
            if post:
                # 해당 포스트를 가져와서
                post = Post.objects.get(pk=pk)
                # 포스트에 연결된 커멘트 트랙들의 쿼리셋 리턴
                return post.comment_tracks.all()
            # 해당 pk값을 가진 포스트가 없으면,
            else:
                # 에러를 발생시킴.
                error = {
                    "detail": "포스트가 존재하지 않습니다."
                }
                raise exceptions.ValidationError(error)
        # POST 요청인 경우 pk 값으로 모든 포스트 쿼리셋 리턴
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


# 커멘트 트랙 디테일 조회, 수정, 삭제 API
class CommentTrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentTrack.objects.all()
    serializer_class = CommentTrackSerializer
    permission_classes = (
        # 작성자 본인에게만 수정, 삭제 권한 부여
        IsAuthorOrReadOnly,
    )
