from django.conf.urls import url

from users.views import sign_in, sign_out

urlpatterns = [
    url(r'^sign-in/$', sign_in, name='sign-in'),
    url(r'^sign-out/$', sign_out, name='sign-out'),
]
