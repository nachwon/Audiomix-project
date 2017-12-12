from django.conf.urls import url

from users.views import UserDetail, Login, Signup, ActivateUser, UserList, FollowUserToggle

urlpatterns = [
    # User Object
    url(r'^$', UserList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='detail'),
    # User Follow
    url(r'^(?P<pk>\d+)/follow/$', FollowUserToggle.as_view(), name='follow'),
    # User Login/Signup
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^activate/$', ActivateUser.as_view(), name='activate'),
]
