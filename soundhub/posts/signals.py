from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

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
        if hasattr(instance,_UNSAVED_POST_IMG):
            instance.post_img = getattr(instance, _UNSAVED_POST_IMG)
        instance.save()
