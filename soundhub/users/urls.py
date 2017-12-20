
from django.conf.urls import url




from users.views import UserDetail, Login, Signup, ActivateUser, UserList, FollowUserToggle, GoogleLogin, FacebookLogin, \
    ProfileImage, Logout

urlpatterns = [
    # User Object
    url(r'^$', UserList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='detail'),
    # User Follow
    url(r'^(?P<pk>\d+)/follow/$', FollowUserToggle.as_view(), name='follow'),
    # User Profile
    url(r'^(?P<pk>\d+)/profile-img/$', ProfileImage.as_view(), name='profile-img'),
    # User Login/Signup
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^activate/$', ActivateUser.as_view(), name='activate'),
    url(r'^google_login/$', GoogleLogin.as_view(), name='google-login'),
    url(r'^facebook_login/$', FacebookLogin.as_view(), name='facebook-login')
]

