from django.conf.urls import url

from posts.views import PostList, PostDetail

urlpatterns = [
    # Post
    url(r'^list/$', PostList.as_view(), name='post-list'),
    url(r'(?P<pk>\d+)/$', PostDetail.as_view(), name='post-detail'),
]
