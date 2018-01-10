from django.conf.urls import url

from users.views import sign_in

urlpatterns = [
    url(r'^sign-in/$', sign_in, name='sign-in'),
]
