import os
from django.core.files.base import ContentFile

from utils.pywave import Waveform

_UNSAVED_AUTHOR_TRACK = 'unsaved_author_track'
_UNSAVED_POST_IMG = 'unsaved_post_img'


# save 메서드가 시작될 때 author_track과 post_img를 저장하지 않고 넘어감
def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk:
        if not hasattr(instance, _UNSAVED_AUTHOR_TRACK):
            setattr(instance, _UNSAVED_AUTHOR_TRACK, instance.author_track)
        if not hasattr(instance, _UNSAVED_POST_IMG):
            setattr(instance, _UNSAVED_POST_IMG, instance.post_img)
        instance.author_track = None
        instance.post_img = None


# save 메서드가 끝나고 난 이후 author_track과 post_img를 할당한 뒤 다시 save 메서드 호출
def save_file(sender, instance, created, **kwargs):
    if created:
        # author_track 오디오 파일 저장
        if hasattr(instance, _UNSAVED_AUTHOR_TRACK):
            instance.author_track = getattr(instance, _UNSAVED_AUTHOR_TRACK)

            # author_track에 대한 웨이브폼 이미지 생성
            file = instance.author_track
            waveform = Waveform(file, file.name)
            waveform_base = waveform.save()
            waveform_cover = waveform.change_color(waveform_base)

            # 웨이브폼 이미지 업로드
            with open(waveform_base, 'rb') as f1:
                base = ContentFile(f1.read())

            with open(waveform_cover, 'rb') as f2:
                cover = ContentFile(f2.read())

            # 필드 저장
            instance.author_track_waveform_base.save('author_track.png', base)
            instance.author_track_waveform_cover.save('author_track_cover.png', cover)

            # 로컬 파일 삭제
            os.remove(waveform_base)
            os.remove(waveform_cover)

        # post_img 저장
        if hasattr(instance, _UNSAVED_POST_IMG):
            instance.post_img = getattr(instance, _UNSAVED_POST_IMG)
        instance.save()
