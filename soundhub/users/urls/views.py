from django.conf.urls import url

from users.views.auth import sign_in, sign_out, facebook_login, sign_up, google_login, sign_up_index
from users.views.user import user_detail, follow_toggle, get_tracks, get_comments

urlpatterns = [
    url(r'^signup-index', sign_up_index, name='signup-index'),
    url(r'^signup/$', sign_up, name='sign-up'),
    url(r'^signin/$', sign_in, name='sign-in'),
    url(r'^fb-login/$', facebook_login, name='fb-login'),
    url(r'^google-login/$', google_login, name='google-login'),
    url(r'^signout/$', sign_out, name='sign-out'),

    url(r'^(?P<pk>\d+)/$', user_detail, name='user-detail'),
    url(r'^(?P<pk>\d+)/tracks/$', get_tracks, name='tracks'),
    url(r'^(?P<pk>\d+)/comments/$', get_comments, name='comments'),
    url(r'^(?P<pk>\d+)/follow/$', follow_toggle, name='follow'),
]
