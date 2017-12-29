import os
import shutil

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pydub import AudioSegment

from django.conf import settings


def save_master_track(self):
    """
    author_track 과 comment_track 들을 S3 저장소에서 바로 불러와 Mix 한 뒤
    로컬에 master_track.mp3 를 생성하고 그것을 다시 읽어서 Post 객체에 전달.
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
        directory = os.path.join(settings.MEDIA_ROOT, f'user_{self.author.pk}/Post_{self.pk}')
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
        # master_track 필드에 저장
        self.master_track.save(
            'master_track.mp3',
            file,
        )
        # 업로드 후 파일 삭제
        shutil.rmtree(directory)



