import os
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.db import models
from pydub import AudioSegment

from config import settings
from config.settings import MEDIA_ROOT


def author_track_directory_path(instance, filename):
    return f'user_{instance.author.id}/Post_{instance.id}/author_track/author_track.mp3'


def master_track_directory_path(instance, filename):
    return f'user_{instance.author.id}/Post_{instance.id}/master_track/master_track.mp3'


def comment_track_directory_path(instance, filename):
    return f'user_{instance.post.author.id}/Post_{instance.post.id}/comment_tracks/comment_track_{instance.pk}.mp3'


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    master_track = models.FileField(upload_to=master_track_directory_path, blank=True, null=True)
    author_track = models.FileField(upload_to=author_track_directory_path, max_length=255)
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

    # master_track 을 생성함
    def save_master_track(self):
        """
        author_track 과 comment_track 들을 S3 저장소에서 바로 불러와 사용하는 것까지는 성공했지만,
        master_track 을 S3 저장소에 바로 생성하는 것은 아직 성공하지 못했음.
        따라서, 로컬에 master_track.mp3 를 생성하고 그것을 다시 읽어서 Post 객체에 전달하는 방식임.
        :return: master_track 의 ContentFile 객체
        """
        # 포스트의 mixed_tracks 필드에 있는 모든 커맨트 트랙 객체들을 가져옴
        mixed_tracks = self.mixed_tracks.all()
        # S3 저장소
        storage = default_storage

        # mixed_tracks 에 객체가 있으면,
        if mixed_tracks.exists():
            # author_track 파일을 s3에서 가져옴
            author_track_dir = f'user_{self.author.id}/Post_{self.pk}/author_track/author_track.mp3'
            author_track = storage.open(author_track_dir, 'r')
            # author_track.mp3 파일을 AudioSegment 객체로 변환
            author_mix = AudioSegment.from_mp3(author_track)

            # 빈 리스트 하나 만들어줌
            mix_list = list()
            # mixed_tracks 안에 있는 객체들을 하나씩 돌면서 연결된 comment_track_pk.mp3 파일을 가져옴
            for track in mixed_tracks:
                comment_track_dir = \
                    f'user_{track.post.author.id}/Post_{track.post.pk}/comment_tracks/comment_track_{track.pk}.mp3'
                comment_track = storage.open(comment_track_dir, 'r')
                # 가져온 파일을 AudioSegment 객체로 변환
                mix = AudioSegment.from_mp3(comment_track)
                # AudioSegment 객체를 mix_list 에 추가함
                mix_list.append(mix)

            # mix_list 안에 있는 AudioSegment 객체를 하나씩 돌면서 author_track.mp3 에 덮어씌움
            for mix in mix_list:
                author_mix = author_mix.overlay(mix)

            # master_track 을 위한 로컬 경로
            directory = os.path.join(MEDIA_ROOT, f'{self.author.nickname}: Post_{self.pk}')
            # 경로가 없으면 만들어줌
            if not os.path.exists(directory):
                os.makedirs(directory)
            master_dir = os.path.join(directory, f'master_track.mp3')

            # 위의 경로로 믹스된 author_mix 객체를 mp3파일로 export 시킴
            author_mix.export(master_dir, format="mp3")

            # 로컬에 저장된 master_track.mp3 를 bytes 로 열고
            with open(master_dir, 'rb') as f:
                master_track = f.read()
            # 장고 ContentFile 객체로 변환하여 리턴
            file = ContentFile(master_track)  # 서상원 Contributed
            return file

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
