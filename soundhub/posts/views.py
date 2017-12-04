from rest_framework import generics
from rest_framework import exceptions
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from posts.models import Post, CommentTrack, PostLike
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


# 포스트 좋아요 & 좋아요 취소 토글
class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()
    permission_classes = (
        # 회원만 좋아요 가능
        IsAuthenticatedOrReadOnly,
    )

    # /post/pk/like/ 에 POST 요청
    def post(self, request, *args, **kwargs):
        # pk 값으로 필터해서 Post 인스턴스 하나 가져옴
        instance = self.get_object()
        # 현재 로그인된 유저. AnonymousUser인 경우 permission에서 거름.
        user = request.user

        # 현재 로그인된 유저가 Post 인스턴스의 liked 목록에 있으면
        if user in instance.liked.all():
            # PostLike 테이블에서 해당 관계 삭제
            liked = PostLike.objects.get(author_id=user.pk, post_id=instance.pk)
            liked.delete()
            instance.num_liked = len(instance.liked.all())
            instance.save()

        # 없으면
        else:
            # PostLike 테이블에서 관계 생성
            PostLike.objects.create(author_id=user.pk, post_id=instance.pk)
            instance.num_liked = len(instance.liked.all())
            instance.save()

        # 업데이트된 instance를 PostSerializer에 넣어 직렬화한 data를 응답으로 돌려줌
        data = {
            "post": PostSerializer(instance).data
        }
        return Response(data)


class HomePageView(ListModelMixin,generics.GenericAPIView):
    post_serializer = PostSerializer

    def list(self, request, *args, **kwargs):
        pop_post_queryset = Post.objects.order_by('-num_liked')[:15]
        recent_post_queryset = Post.objects.order_by('-created_date')[:15]

        pop_post_serializer = self.post_serializer(pop_post_queryset, many=True)
        recent_post_serializer = self.post_serializer(recent_post_queryset, many=True)

        data = {
            "pop_posts": pop_post_serializer.data,
            "recent_posts": recent_post_serializer.data
        }
        return Response(data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



