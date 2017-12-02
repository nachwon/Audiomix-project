from django.conf.urls import url

from posts.views import PostList, PostDetail, CommentTrackList, CommentTrackDetail

urlpatterns = [
    # Post
    url(r'^$', PostList.as_view(), name='post-list'),
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='post-detail'),

    # Comment_track
    url(r'^(?P<pk>\d+)/comments/$', CommentTrackList.as_view(), name='comment-track-list'),
    url(r'^comment/(?P<pk>\d+)/$', CommentTrackDetail.as_view(), name='comment-track-detail')
]
