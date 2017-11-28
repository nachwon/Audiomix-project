from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

INSTRUMENT_CHOICES = (
        ('G', 'Guitar'),
        ('B', 'Bass'),
        ('D', 'Drums'),
        ('V', 'Vocals'),
        ('K', 'Keyboard'),
        ('O', 'Others'),
    )


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=1, choices=INSTRUMENT_CHOICES)
    master_track = models.FileField(upload_to='master_tracks', blank=True, null=True)
    author_track = models.FileField(upload_to='author_tracks')

    def __str__(self):
        return f'{self.title} - {self.author}'


class CommentTrack(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment_tracks', on_delete=models.CASCADE)
    comment_track = models.FileField(upload_to='comment_tracks')
    instrument = models.CharField(max_length=1, choices=INSTRUMENT_CHOICES)

    def __str__(self):
        return f'{self.post.title}: {self.instrument}'
