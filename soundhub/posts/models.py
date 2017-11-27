from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

INSTRUMENT_CHOICES = (
        ('G', 'Guitar'),
        ('B', 'Base'),
        ('D', 'Drums'),
        ('V', 'Vocals'),
        ('K', 'Keyboard'),
        ('O', 'Others'),
    )


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=1, choices=INSTRUMENT_CHOICES)
    master_track = models.FileField(upload_to='master_tracks')


class CommentTrack(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_track = models.FileField(upload_to='comment_tracks')
    instrument = models.CharField(max_length=1, choices=INSTRUMENT_CHOICES)
