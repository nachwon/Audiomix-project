from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework import exceptions
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

    # author_track 저장 폴더 경로의 동적 생성에 포스트 pk 값을 사용하기 위한 create 메서드 오버라이드
    def create(self, request, *args, **kwargs):
        # author_track 을 제외한 모든 정보
        data = {
            "title": request.data.get('title'),
            "instrument": request.data.get('instrument'),
            "genre": request.data.get('genre')
        }
        # 정보를 시리얼라이저에 전달하여 객체화
        serializer = self.get_serializer(data=data)
        # is_valid 를 통해 데이터 검증
        # author_track 의 required=False 때문에 author_track 이 없어도 통과함.
        serializer.is_valid(raise_exception=True)
        # 저장해서 포스트 pk 값 할당
        serializer.save(author=self.request.user)
        # perform_create 메서드를 호출해서 author_track 포함하여 저장
        # 포스트에 pk 값이 할당되었으므로, author_track 을 저장할 때 경로에 pk 값을 사용할 수 있다.
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # author_track 이 없으면 에러 발생
        if self.request.data.get('author_track', False):
            serializer.save(author_track=self.request.data.get('author_track'))
        else:
            data = {
                "detail": "author_track 파일이 제출되지 않았습니다."
            }
            raise exceptions.ValidationError(data)


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
        post.save_num_comments()  # 코멘트 갯수 업데이트


# 커멘트 트랙 디테일 조회, 수정, 삭제 API
class CommentTrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentTrack.objects.all()
    serializer_class = CommentTrackSerializer
    permission_classes = (
        # 작성자 본인에게만 수정, 삭제 권한 부여
        IsAuthorOrReadOnly,
    )

    # CommentTrack 삭제시 연결된 Post의 num_comments - 1 을 해주고 삭제
    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.post.num_comments -= 1
        comment.post.save()
        return self.destroy(request, *args, **kwargs)


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
            instance.save_num_liked()  # Post의 num_liked 업데이트
            instance.author.save_total_liked()  # User의 total_liked 업데이트

        # 없으면
        else:
            # PostLike 테이블에서 관계 생성
            PostLike.objects.create(author_id=user.pk, post_id=instance.pk)
            instance.save_num_liked()  # Post의 num_liked 업데이트
            instance.author.save_total_liked()  # User의 total_liked 업데이트

        # 업데이트된 instance를 PostSerializer에 넣어 직렬화하여 응답으로 돌려줌
        data = PostSerializer(instance).data
        return Response(data)


class MixTracks(generics.UpdateAPIView, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )

    def patch(self, request, *args, **kwargs):
        # mix_tracks 라는 키값으로 들어온 데이터를 확인.
        # mix_tracks 에는 ,로 구분된 커멘트 트랙의 pk 값을 전달해야 함. ex) 54, 55
        mixed_tracks_raw = request.data.get('mix_tracks', False)
        # 데이터가 있으면,
        if mixed_tracks_raw:
            # pk 값으로 포스트를 가져온다.
            post = self.get_object()
            # 가져온 포스트에 연결된 모든 커맨트 트랙 리스트를 가져온다.
            queryset = post.comment_tracks.all()
            # 한 덩어리의 문자열에서 공백 문자를 제거하고 ,를 기준으로 분리하여 리스트로 만든다.
            # ex) "54, 55" -> [54, 55]
            mixed_tracks = mixed_tracks_raw.replace(' ', '').split(',')
            # 기존의 mixed_tracks 값을 모두 제거해준다.
            post.mixed_tracks.clear()
            # 에러 메세지를 담기 위한 리스트 생성
            error_msg = list()

            # mixed_tracks 의 값을 하나씩 돌면서
            for pk in mixed_tracks:
                try:
                    # 커맨트 트랙 객체를 가져와서
                    comment = post.comment_tracks.get(pk=pk)
                    # 포스트 객체의 mixed_tracks 관계 필드에 추가한다.
                    post.mixed_tracks.add(comment)

                # 값을 못 가져오는 경우, 즉, 해당 포스트에 연결된 커멘트 트랙 중 하나의 pk 가 아닌 경우
                except ObjectDoesNotExist:
                    # 에러 메세지 리스트에 못 찾은 pk 값 전달.
                    error_msg.append(pk)
                    continue

            # 에러 메세지 리스트가 비어있지 않으면,
            if bool(error_msg):
                # 에러 일으키면서 에러 메세지 전달
                raise exceptions.NotFound(f'찾을 수 없습니다: 코멘트 트랙 {", ".join(error_msg)}')

            # 에러가 없으면 포스트 상태 저장
            post.save()

            # 모든 커멘트 트랙들 돌면서 is_mixed 값 업데이트
            for i in queryset:
                i.save_is_mixed()

            master_track = post.save_master_track()
            post.master_track.save(
                'master_track.mp3',
                master_track,
            )

        else:
            post = self.get_object()
            queryset = post.comment_tracks.all()
            post.mixed_tracks.clear()
            # 모든 커멘트 트랙들 돌면서 is_mixed 값 업데이트
            for i in queryset:
                i.save_is_mixed()

        # 나머지 필드들에 대해서는 기존의 PATCH 요청과 동일
        return self.partial_update(request, *args, **kwargs)


