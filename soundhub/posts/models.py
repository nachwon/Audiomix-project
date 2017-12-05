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
    num_liked = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

    # 자신을 좋아요한 횟수를 num_liked 필드에 저장
    def save_num_liked(self):
        self.num_liked = self.liked.count()
        self.save()

    # 자신에게 연결된 코멘트들의 갯수를 num_comments 필드에 저장
    def save_num_comments(self):
        self.num_comments = self.comment_tracks.count()
        self.save()

    class Meta:
        ordering = ['-created_date']


class CommentTrack(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment_tracks', on_delete=models.CASCADE)
    comment_track = models.FileField(upload_to='comment_tracks', max_length=255)
    instrument = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.post.title}: {self.instrument}'

    class Meta:
        ordering = ('-created_date',)


class PostLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} liked {self.post}'

    class Meta:
        ordering = ['-liked_date']
