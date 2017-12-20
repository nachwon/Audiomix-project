from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, CommentTrack
from posts.serializers import PostSerializer, CommentTrackSerializer
from users.serializers import UserSerializer

User = get_user_model()


class Search(APIView):
    def get(self, request):
        keyword = request.GET['keyword']

        def get_list(queryset, serializer):
            l = list()
            for content in queryset:
                l.append(serializer(content).data)
            return l

        users = User.objects.filter(nickname__icontains=keyword)
        posts_by_title = Post.objects.filter(title__icontains=keyword)
        posts_by_author = Post.objects.filter(author__nickname__icontains=keyword)
        comment_tracks = CommentTrack.objects.filter(author__nickname__icontains=keyword)

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
