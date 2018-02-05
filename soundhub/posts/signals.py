from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

_UNSAVED_FILEFIELD = 'unsaved_filefield'


def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk and not hasattr(instance, _UNSAVED_FILEFIELD):
        setattr(instance, _UNSAVED_FILEFIELD, instance.author_track)
        instance.author_track = None


def save_file(sender, instance, created, **kwargs):
    if created and hasattr(instance, _UNSAVED_FILEFIELD):
        instance.author_track = getattr(instance, _UNSAVED_FILEFIELD)
        instance.save()