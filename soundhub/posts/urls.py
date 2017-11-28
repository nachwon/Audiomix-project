from django.conf.urls import url

from posts.views import PostList, PostDetail, CommentTrackList

urlpatterns = [
    # Post
    url(r'^$', PostList.as_view(), name='post-list'),
    url(r'(?P<pk>\d+)/$', PostDetail.as_view(), name='post-detail'),

    # Comment_track
    url(r'(?P<pk>\d+)/comment/$', CommentTrackList.as_view(), name='comment-track-list'),
]
