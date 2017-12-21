from django.conf import settings
from django.db import models


class Message(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True,
                                  related_name='sent_msgs',
                                  on_delete=models.SET_NULL)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='received_msgs',
                                null=True,
                                on_delete=models.SET_NULL)
    content = models.CharField(max_length=255, blank=True, null=True)
    read_date = models.DateTimeField(default=None, null=True)
    sent_deleted = models.BooleanField(default=False)
    inbox_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'from: {self.from_user}, to: {self.to_user}, content: {self.content}'
