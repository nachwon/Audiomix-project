from django.conf.urls import url

from users.views import UserDetail, UserSignup, UserLogin

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^signup/$', UserSignup.as_view(), name='user-signup'),
    url(r'^login/$', UserLogin.as_view(), name='user-login'),
]
