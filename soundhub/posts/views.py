import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import TemporaryUploadedFile
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status, filters
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from posts.models import Post, CommentTrack, PostLike
from posts.serializers import PostSerializer, CommentTrackSerializer
from posts.tasks import mix_task

from utils.permissions import IsAuthorOrReadOnly
from utils.rescale_img import make_post_img


# 포스트 목록 조회 및 포스트 생성 API
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        # 회원인 경우만 포스트 작성 가능
        IsAuthenticatedOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = (
        'instrument',
        'genre',
    )
    ordering_fields = (
        'num_liked',
        'num_comments',
        'created_date',
    )

    # author_track 저장 폴더 경로의 동적 생성에 포스트 pk 값을 사용하기 위한 create 메서드 오버라이드
    def create(self, request, *args, **kwargs):
        # author_track 을 제외한 모든 정보
        data = {
            "title": request.data.get('title'),
            "instrument": request.data.get('instrument'),
            "genre": request.data.get('genre'),
            "bpm": request.data.get('bpm'),
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
        post_img = self.request.data.get('post_img', None)
        if post_img is not None and type(post_img) == TemporaryUploadedFile:
            file, post_dir = make_post_img(post_img)
            serializer.save(post_img=file)
            os.remove(post_dir)

        elif post_img is not None and not type(post_img) == TemporaryUploadedFile:
            data = {
                "post_img": "올바른 형식의 파일이 제출되지 않았습니다."
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

    # 포스트 수정
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        post_img = request.data.get('post_img', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 요청에 포스트 이미지가 있을 경우
        if post_img:
            # 포스트 이미지 크기 수정 후 업로드
            file, post_dir = make_post_img(post_img=post_img)
            instance.post_img.save(
                'post_bg.png',
                file,
            )
            os.remove(post_dir)

        # 포스트 이미지 필드에 빈 스트링이 오면,
        elif post_img == "":
            # 인스턴스의 포스트 이미지 삭제
            instance.post_img.delete()
        # 요청에 포스트 이미지 필드가 없는 경우
        else:
            # 일반적인 포스트 수정 수행
            self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # 포스트 객체 삭제시 s3 저장소 내의 파일들도 모두 삭제
    def perform_destroy(self, instance):
        instance.author_track.delete()
        instance.master_track.delete()
        # 연결된 모든 커멘트 트랙 객체의 파일들도 삭제
        comment_set = instance.comment_tracks.all()
        for i in comment_set:
            i.comment_track.delete()
        instance.delete()


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
    def create(self, request, *args, **kwargs):
        post = self.get_object()
        data = {
            "instrument": request.data.get('instrument')
        }
        serializer = self.get_serializer(data=data)
        # is_valid 를 통해 데이터 검증
        # author_track 의 required=False 때문에 author_track 이 없어도 통과함.
        serializer.is_valid(raise_exception=True)
        # 저장해서 포스트 pk 값 할당
        serializer.save(author=self.request.user, post=post)
        # perform_create 메서드를 호출해서 author_track 포함하여 저장
        # 포스트에 pk 값이 할당되었으므로, author_track 을 저장할 때 경로에 pk 값을 사용할 수 있다.
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        post = self.get_object()
        if self.request.data.get('comment_track', False):
            serializer.save(
                comment_track=self.request.data.get('comment_track')
            )
        else:
            data = {
                "detail": "코멘트 트랙이 제출되지 않았습니다."
            }
            raise exceptions.ValidationError(data)
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

    def perform_destroy(self, instance):
        instance.comment_track.delete()
        instance.delete()


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

            # 셀러리를 사용한 비동기 처리로 음원 파일 믹스
            mix_task.delay(post.pk)

        # mix_tracks 키로 넘어온 값이 없으면
        else:
            # 포스트 객체 가져와서
            post = self.get_object()
            # 객체의 master_track 을 author_track 과 동일하게 만들어 주고
            post.master_track = post.author_track
            # 저장
            post.save()
            # mixed_tracks 필드를 비워준다
            post.mixed_tracks.clear()

            # 포스트에 달린 모든 커멘트 트랙들을 불러와서
            queryset = post.comment_tracks.all()
            # 하나씩 돌면서 is_mixed 값 업데이트
            for i in queryset:
                i.save_is_mixed()

        # 나머지 필드들에 대해서는 기존의 PATCH 요청과 동일
        return self.partial_update(request, *args, **kwargs)


