import re

from django.db import models

from django.conf import settings


def extension(filename):
    p = re.compile(r'.*[.](.*)')
    ext = p.match(filename).group(1)
    return ext


def author_track_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.author.id}/Post_{instance.id}/author_track/author_track.{ext}'


def master_track_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.author.id}/Post_{instance.id}/master_track/master_track.{ext}'


def comment_track_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.post.author.id}/Post_{instance.post.id}/comment_tracks/comment_track_{instance.pk}.{ext}'


def post_img_directory_path(instance, filename):
    return f'user_{instance.author.id}/Post_{instance.id}/post_img/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_img = models.ImageField(upload_to=post_img_directory_path, blank=True)
    instrument = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    master_track = models.FileField(upload_to=master_track_directory_path, blank=True, null=True)
    author_track = models.FileField(upload_to=author_track_directory_path, max_length=255)
    bpm = models.IntegerField(default=0)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through='PostLike',
                                   related_name='liked_posts')
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
    mixed_to = models.ForeignKey(Post, related_name='mixed_tracks',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    is_mixed = models.NullBooleanField(default=False)
    comment_track = models.FileField(upload_to=comment_track_directory_path, max_length=255)
    instrument = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.post.title}: {self.instrument}'

    class Meta:
        ordering = ('-created_date',)

    # 커맨트 트랙의 믹스 여부에 따라 is_mixed 값을 바꿔줌
    def save_is_mixed(self):
        if self.mixed_to is not None:
            self.is_mixed = True
        else:
            self.is_mixed = False
        self.save()
        return self.is_mixed


class PostLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.author} liked {self.post}'

    class Meta:
        ordering = ['-liked_date']
