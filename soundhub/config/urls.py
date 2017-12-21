"""soundhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from config.views import redirect_to_home
from utils.search import Search


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', redirect_to_home, name='homepage'),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^user/', include('users.urls', namespace='user')),
    url(r'^post/', include('posts.urls', namespace='post')),
    url(r'^home/', include('homepages.urls', namespace='home')),
    url(r'^message/', include('messages.urls', namespace='message')),

    # 특정 기능을 간단히 테스트할 때 쓰는 주소
    # url(r'^test/$', Test.as_view(), name='test'),
]
