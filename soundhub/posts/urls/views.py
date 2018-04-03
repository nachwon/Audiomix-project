from django.conf.urls import url

from posts.views import like_toggle, post_detail

from posts import ajax_views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', post_detail, name='post-detail'),
    url(r'^(?P<pk>\d+)/like/$', like_toggle, name='like'),

    url(r'^comment/(?P<pk>\d+)/$', ajax_views.SendCommentTrack.as_view()),
    url(r'^(?P<pk>\d+)/author-track/$', ajax_views.SendAuthorTrack.as_view())
]
