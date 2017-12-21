from django.conf.urls import url

from direct_messages.views import SendMessage

urlpatterns = [
    url(r'^$', SendMessage.as_view(), name='direct-messages')
]
