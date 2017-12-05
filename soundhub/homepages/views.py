from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostSerializer


class HomePageView(ListModelMixin, generics.GenericAPIView):
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
