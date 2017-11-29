from django.conf.urls import url

from users import apis
from users.views import UserDetail

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
    # url(r'^signup/$', UserSignup.as_view(), name='user-signup'),
    url(r'^login/$', apis.Login.as_view(), name='login'),
    url(r'^signup/$', apis.Signup.as_view(), name='signup'),
    url(r'^activate/$', apis.ActivateUser.as_view(), name='activate'),

]
