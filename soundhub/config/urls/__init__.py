from django.conf.urls import url, include

from . import views, apis

urlpatterns = [
    url(r'^', include(views, namespace='views')),
    url(r'^api/', include(apis, namespace='apis')),
]
