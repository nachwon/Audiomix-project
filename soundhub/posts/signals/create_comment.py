import os
from django.core.files.base import ContentFile

from utils.pywave import Waveform

_UNSAVED_COMMENT_TRACK = 'unsaved_comment_track'


# save 메서드가 시작될 때 comment_track을 저장하지 않고 넘어감
def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk:
        if not hasattr(instance, _UNSAVED_COMMENT_TRACK):
            setattr(instance, _UNSAVED_COMMENT_TRACK, instance.comment_track)
        instance.comment_track = None


# save 메서드가 끝나고 난 이후 comment_track을 할당한 뒤 다시 save 메서드 호출
def save_file(sender, instance, created, **kwargs):
    if created:
        # comment_track 오디오 파일 저장
        if hasattr(instance, _UNSAVED_COMMENT_TRACK):
            instance.comment_track = getattr(instance, _UNSAVED_COMMENT_TRACK)

            # comment_track에 대한 웨이브폼 이미지 생성
            file = instance.comment_track
            waveform = Waveform(file, file.name)
            waveform_base = waveform.save()
            waveform_cover = waveform.change_color(waveform_base)

            # 웨이브폼 이미지 업로드
            with open(waveform_base, 'rb') as f1:
                base = ContentFile(f1.read())

            with open(waveform_cover, 'rb') as f2:
                cover = ContentFile(f2.read())

            # 필드 저장
            instance.comment_track_waveform_base.save('comment_track.png', base)
            instance.comment_track_waveform_cover.save('comment_track_cover.png', cover)

            # 로컬 파일 삭제
            os.remove(waveform_base)
            os.remove(waveform_cover)

        instance.save()
