from django.conf.urls import url

from posts.views import PostList

urlpatterns = [
    # Post
    url(r'^list/$', PostList.as_view(), name='post-list'),
]
