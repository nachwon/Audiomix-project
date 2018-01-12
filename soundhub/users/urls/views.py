from django.conf.urls import url

from users.views import sign_in, sign_out, facebook_login

urlpatterns = [
    url(r'^sign-in/$', sign_in, name='sign-in'),
    url(r'^fb-login/$', facebook_login, name='fb-login'),
    url(r'^sign-out/$', sign_out, name='sign-out'),
]
