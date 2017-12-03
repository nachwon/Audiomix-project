from django.conf.urls import url

from posts.views import PostList, PostDetail, CommentTrackList, CommentTrackDetail, PostLikeToggle

urlpatterns = [
    # Post
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='detail'),
    # PostLike
    url(r'^(?P<pk>\d+)/like/$', PostLikeToggle.as_view(), name='like'),
    # Comment_track
    url(r'^(?P<pk>\d+)/comments/$', CommentTrackList.as_view(), name='comment-track-list'),
    url(r'^comment/(?P<pk>\d+)/$', CommentTrackDetail.as_view(), name='comment-track-detail'),
]
