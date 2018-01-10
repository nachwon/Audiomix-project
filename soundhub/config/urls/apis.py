from django.conf.urls import url, include

from config.views import redirect_to_home
from utils.search import Search

urlpatterns = [
    url(r'^$', redirect_to_home, name='homepage'),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^user/', include('users.urls.apis', namespace='user')),
    url(r'^post/', include('posts.urls', namespace='post')),
    url(r'^home/', include('homepages.urls', namespace='home')),
    url(r'^message/', include('direct_messages.urls', namespace='message')),
]
