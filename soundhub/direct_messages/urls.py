from django.conf.urls import url

from direct_messages.views import SendMessage, Inbox, Sent

urlpatterns = [
    url(r'^$', SendMessage.as_view(), name='direct-messages'),
    url(r'^inbox/$', Inbox.as_view(), name='inbox'),
    url(r'^sent/$', Sent.as_view(), name='sent'),
]
