import os
from django.core.files.base import ContentFile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from utils.pywave import Waveform

_UNSAVED_AUTHOR_TRACK = 'unsaved_author_track'
_UNSAVED_POST_IMG = 'unsaved_post_img'


def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk:
        if not hasattr(instance, _UNSAVED_AUTHOR_TRACK):
            setattr(instance, _UNSAVED_AUTHOR_TRACK, instance.author_track)
        if not hasattr(instance, _UNSAVED_POST_IMG):
            setattr(instance, _UNSAVED_POST_IMG, instance.post_img)
        instance.author_track = None
        instance.post_img = None


def save_file(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, _UNSAVED_AUTHOR_TRACK):
            instance.author_track = getattr(instance, _UNSAVED_AUTHOR_TRACK)
            file = instance.author_track
            waveform = Waveform(file, file.name)
            waveform_base = waveform.save()
            waveform_cover = waveform.change_color(waveform_base)

            with open(waveform_base, 'rb') as f1:
                base = ContentFile(f1.read())

            with open(waveform_cover, 'rb') as f2:
                cover = ContentFile(f2.read())

            instance.author_track_waveform_base.save('author_track.png', base)
            instance.author_track_waveform_cover.save('author_track_cover.png', cover)

            os.remove(waveform_base)
            os.remove(waveform_cover)

        if hasattr(instance, _UNSAVED_POST_IMG):
            instance.post_img = getattr(instance, _UNSAVED_POST_IMG)
        instance.save()
