from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage as storage

from posts.models import Post
from utils.pywave import Waveform


class Command(BaseCommand):
    help = 'Creates waveform image from an audio file source'

    def handle(self, *args, **options):

        posts = Post.objects.all()
        for post in posts:
            audio_dir = post.author_track.url
            audio_track = storage.open(audio_dir, 'r')
            waveform = Waveform(audio_track)
            waveform_base = waveform.save()
            waveform_cover = waveform.change_color(waveform_base)

            with open(waveform_base, 'rb') as f1:
                base = ContentFile(f1.read())

            with open(waveform_cover, 'rb') as f2:
                cover = ContentFile(f2.read())

            post.author_track_waveform_base.save('author_track.png', base)
            post.author_track_waveform_cover.save('author_track_cover.png', cover)

            post.save()
