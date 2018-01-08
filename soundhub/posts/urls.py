from django.conf.urls import url

from posts.apis import PostList, PostDetail, CommentTrackList, CommentTrackDetail, PostLikeToggle, MixTracks

urlpatterns = [
    # Post
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='detail'),
    # MixTracks
    url(r'^(?P<pk>\d+)/mix/$', MixTracks.as_view(), name='mix-tracks'),
    # PostLike
    url(r'^(?P<pk>\d+)/like/$', PostLikeToggle.as_view(), name='like'),
    # Comment_track
    url(r'^(?P<pk>\d+)/comments/$', CommentTrackList.as_view(), name='comment-track-list'),
    url(r'^comment/(?P<pk>\d+)/$', CommentTrackDetail.as_view(), name='comment-track-detail'),
]
