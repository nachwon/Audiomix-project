from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from homepages.serializers import HomePageUserSerializer, HomepagePostSerializer
from posts.models import Post

User = get_user_model()


class HomePageView(ListModelMixin, generics.GenericAPIView):
    user_serializer = HomePageUserSerializer
    post_serializer = HomepagePostSerializer

    def list(self, request, *args, **kwargs):
        pop_user_queryset = User.objects.order_by('-total_liked')[:15]
        pop_post_queryset = Post.objects.order_by('-num_liked')[:15]
        recent_post_queryset = Post.objects.order_by('-created_date')[:15]

        pop_user_serializer = self.user_serializer(pop_user_queryset, many=True)
        pop_post_serializer = self.post_serializer(pop_post_queryset, many=True)
        recent_post_serializer = self.post_serializer(recent_post_queryset, many=True)

        data = {
            "pop_users": pop_user_serializer.data,
            "pop_posts": pop_post_serializer.data,
            "recent_posts": recent_post_serializer.data
        }
        return Response(data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GenreHomePageView(ListModelMixin, generics.GenericAPIView):
    user_serializer = HomePageUserSerializer
    post_serializer = HomepagePostSerializer
    lookup_url_kwarg = 'genre'

    def list(self, request, *args, **kwargs):
        genre = self.kwargs.get(self.lookup_url_kwarg)
        user_queryset = User.objects.filter(genre=genre)
        post_queryset = Post.objects.filter(genre=genre)

        pop_user_queryset = user_queryset.order_by('-total_liked')[:15]
        pop_post_queryset = post_queryset.order_by('-num_liked')[:15]
        recent_post_queryset = post_queryset.order_by('-created_date')[:15]

        pop_user_serializer = self.user_serializer(pop_user_queryset, many=True)
        pop_post_serializer = self.post_serializer(pop_post_queryset, many=True)
        recent_post_serializer = self.post_serializer(recent_post_queryset, many=True)

        data = {
            "total_users": user_queryset.count(),
            "total_posts": post_queryset.count(),
            "pop_users": pop_user_serializer.data,
            "pop_posts": pop_post_serializer.data,
            "recent_posts": recent_post_serializer.data
        }
        return Response(data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class InstrumentHomePageView(ListModelMixin, generics.GenericAPIView):
    user_serializer = HomePageUserSerializer
    post_serializer = HomepagePostSerializer
    lookup_url_kwarg = 'instrument'

    def list(self, request, *args, **kwargs):
        instrument = self.kwargs.get(self.lookup_url_kwarg)
        post_queryset = Post.objects.filter(instrument=instrument)
        user_queryset = User.objects.filter(instrument=instrument)

        pop_user_queryset = user_queryset.order_by('-total_liked')[:15]
        pop_post_queryset = post_queryset.order_by('-num_liked')[:15]
        recent_post_queryset = post_queryset.order_by('-created_date')[:15]

        pop_user_serializer = self.user_serializer(pop_user_queryset, many=True)
        pop_post_serializer = self.post_serializer(pop_post_queryset, many=True)
        recent_post_serializer = self.post_serializer(recent_post_queryset, many=True)

        data = {
            "total_users": user_queryset.count(),
            "total_posts": post_queryset.count(),
            "pop_users": pop_user_serializer.data,
            "pop_posts": pop_post_serializer.data,
            "recent_posts": recent_post_serializer.data
        }
        return Response(data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
