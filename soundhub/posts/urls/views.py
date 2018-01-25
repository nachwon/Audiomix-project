from django.conf.urls import url

from posts.views import like_toggle

urlpatterns = [
    url(r'^(?P<pk>\d+)/like/$', like_toggle, name='like'),
]
