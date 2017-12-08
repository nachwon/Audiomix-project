import os
import requests

from django.db import models
from django.db.models.manager import BaseManager
from pydub import AudioSegment

from config import settings
from config.settings import MEDIA_ROOT


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    master_track = models.FileField(upload_to='master_tracks', blank=True, null=True)
    author_track = models.FileField(upload_to='author_tracks', max_length=255)
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

    def save_master_track(self):
        mixed_tracks = self.mixed_tracks.all()
        author_track = self.author_track
        if mixed_tracks.exists():
            author_track_response = requests.get(author_track.url)
            directory = os.path.join(MEDIA_ROOT, f'{self.author.nickname}: Post_{self.pk}')
            if not os.path.exists(directory):
                os.makedirs(directory)
            author_track_dir = os.path.join(directory, 'author_track.mp3')
            with open(author_track_dir, 'wb') as f:
                f.write(author_track_response.content)
            mix_list = list()
            author_mix = AudioSegment.from_mp3(author_track_dir)

            for track in mixed_tracks:
                comment_track_response = requests.get(track.comment_track.url)
                comment_dir = os.path.join(directory, f'comment_track_{track.pk}.mp3')
                with open(comment_dir, 'wb') as f:
                    f.write(comment_track_response.content)
                mix = AudioSegment.from_mp3(comment_dir)
                mix_list.append(mix)

            for mix in mix_list:
                author_mix = author_mix.overlay(mix)
            master_dir = os.path.join(directory, f'master_track.mp3')

            author_mix.export(master_dir, format="mp3")

            with open(master_dir, 'rb') as f:
                master_track = f

            return master_track

    class Meta:
        ordering = ['-created_date']


class CommentTrack(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment_tracks', on_delete=models.CASCADE)
    mixed_to = models.ForeignKey(Post, related_name='mixed_tracks',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    is_mixed = models.NullBooleanField(default=False)
    comment_track = models.FileField(upload_to='comment_tracks', max_length=255)
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
