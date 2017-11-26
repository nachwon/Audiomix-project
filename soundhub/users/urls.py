from django.conf.urls import url

from users.views import UserDetail

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
]
