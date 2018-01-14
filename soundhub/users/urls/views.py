from django.conf.urls import url

from users.views import sign_in, sign_out, facebook_login, user_detail, sign_up

urlpatterns = [
    url(r'^sign-up/$', sign_up, name='sign-up'),
    url(r'^sign-in/$', sign_in, name='sign-in'),
    url(r'^fb-login/$', facebook_login, name='fb-login'),
    url(r'^sign-out/$', sign_out, name='sign-out'),
    url(r'^(?P<pk>\d+)/$', user_detail, name='user-detail'),
]
