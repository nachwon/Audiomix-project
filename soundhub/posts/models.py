from django.db import models

from config import settings


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    master_track = models.FileField(upload_to='master_tracks', blank=True, null=True)
    author_track = models.FileField(upload_to='author_tracks', max_length=255)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='liked_posts'
    )
    created_data = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        ordering = ['-created_data']


class CommentTrack(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment_tracks', on_delete=models.CASCADE)
    comment_track = models.FileField(upload_to='comment_tracks', max_length=255)
    instrument = models.CharField(max_length=100)
    created_data = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.post.title}: {self.instrument}'

    class Meta:
        ordering = ('-created_data',)


class PostLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} liked {self.post}'

    class Meta:
        ordering = ['-liked_date']
