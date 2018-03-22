import uuid

from django.db import models

from django.conf import settings

from posts.directory_path import *
from users.models import Instrument, Genre


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_img = models.ImageField(upload_to=post_img_directory_path, blank=True)
    instrument = models.ForeignKey(Instrument, related_name='post_instrument', blank=True, null=True, on_delete=models.SET_NULL)
    genre = models.ManyToManyField(Genre, related_name='post_genre', blank=True)

    master_track = models.FileField(upload_to=master_track_directory_path, blank=True, null=True)
    master_track_waveform_base = models.ImageField(
        upload_to=master_track_waveform_base_directory_path, blank=True, null=True
    )
    master_track_waveform_cover = models.ImageField(
        upload_to=master_track_waveform_cover_directory_path, blank=True, null=True
    )

    author_track = models.FileField(upload_to=author_track_directory_path, max_length=255)
    author_track_waveform_base = models.ImageField(
        upload_to=author_track_waveform_base_directory_path, blank=True, null=True
    )
    author_track_waveform_cover = models.ImageField(
        upload_to=author_track_waveform_cover_directory_path, blank=True, null=True
    )

    bpm = models.IntegerField(default=0)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through='PostLike',
                                   related_name='liked_posts')
    num_liked = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

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
    comment_track_waveform_base = models.ImageField(
        upload_to=comment_track_waveform_base_directory_path, blank=True, null=True
    )
    comment_track_waveform_cover = models.ImageField(
        upload_to=comment_track_waveform_cover_directory_path, blank=True, null=True
    )
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.post.title}: {self.instrument.name}'

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


class CommentLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentTrack, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.author} liked {self.comment.post}-{self.comment}'

    class Meta:
        ordering = ['-liked_date']
