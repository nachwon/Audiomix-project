from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, CommentTrack
from posts.serializers import PostSerializer, CommentTrackSerializer
from users.exceptions import RequestDataDoesNotExist
from users.serializers import UserSerializer

User = get_user_model()


class Search(APIView):
    def get(self, request):
        """
        검색어를 받아 DB 에서 검색해서 검색된 객체를 리스트로 반환

        :param request:
            GET = {
                'keyword': 검색어
            }
        :return: 검색된 객체 리스트
        """
        # request 에 전달된 keyword 검사
        # keyword 가 빈 스트링일 경우에도 에러 메세지 호출 (빈스트링으로 검색하면 모든 결과가 나오므로)
        keyword = request.GET['keyword'] if 'keyword' in request.GET else None
        if not keyword:
            raise RequestDataDoesNotExist('검색어가 없습니다')

        # Cls.objects.filter 의 queryset 을 그 안에 있는 객체의 '직렬화 값 리스트'로 변환
        def get_list(queryset, serializer):
            l = list()
            for content in queryset:
                l.append(serializer(content).data)
            return l

        # 각각의 모델에서 검색
        users = User.objects.filter(nickname__icontains=keyword)
        posts_by_title = Post.objects.filter(title__icontains=keyword)
        posts_by_author = Post.objects.filter(author__nickname__icontains=keyword)
        comment_tracks = CommentTrack.objects.filter(author__nickname__icontains=keyword)

        # 검색 결과로 나온 객체들의 직렬화 리스트
        user_list = get_list(users, UserSerializer)
        posts_by_title_list = get_list(posts_by_title, PostSerializer)
        posts_by_author_list = get_list(posts_by_author, PostSerializer)
        comment_track_list = get_list(comment_tracks, CommentTrackSerializer)

        data = {
            'users': user_list,
            'posts_by_title': posts_by_title_list,
            'posts_by_author': posts_by_author_list,
            'comment_tracks': comment_track_list,
        }
        return Response(data, status=status.HTTP_200_OK)
