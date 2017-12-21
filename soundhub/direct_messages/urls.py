from django.conf.urls import url

from direct_messages.views import SendMessage, Inbox, Sent, InboxDetail, SentDetail

urlpatterns = [
    url(r'^$', SendMessage.as_view(), name='direct-messages'),
    url(r'^inbox/$', Inbox.as_view(), name='inbox'),
    url(r'^inbox/(?P<pk>\d+)/$', InboxDetail.as_view(), name='inbox-detail'),
    url(r'^sent/$', Sent.as_view(), name='sent'),
    url(r'^sent/(?P<pk>\d+)/$', SentDetail.as_view(), name='sent-detail'),
]
