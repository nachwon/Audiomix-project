from django.conf.urls import url

from posts.views import like_toggle, post_detail

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', post_detail, name='post-detail'),
    url(r'^(?P<pk>\d+)/like/$', like_toggle, name='like'),
]
