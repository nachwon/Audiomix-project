import re

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage as storage
from pydub.exceptions import CouldntDecodeError

from posts.models import Post
from utils.pywave import Waveform


class Command(BaseCommand):
    help = 'Creates waveform image from an audio file source'

    def handle(self, *args, **options):

        url_parser = re.compile(r".*?/media/(.*)[?].*")

        posts = Post.objects.all()
        for post in posts:
            audio_dir = post.author_track.url
            audio_file = url_parser.search(audio_dir).group(1)
            try:
                cover_png = post.author_track_waveform_cover.url
                cover_png_parsed = url_parser.search(cover_png).group(1)
                print(f'{cover_png_parsed} exists')
                continue
            except ValueError:
                audio_track = storage.open(audio_file, 'r')

            try:
                waveform = Waveform(audio_track, audio_track.name)
            except CouldntDecodeError:
                print(f'CoudntDecodeError raised!: user_{post.author.pk}/Post_{post.pk}')
                continue

            waveform_base = waveform.save()
            waveform_cover = waveform.change_color(waveform_base)

            with open(waveform_base, 'rb') as f1:
                base = ContentFile(f1.read())

            with open(waveform_cover, 'rb') as f2:
                cover = ContentFile(f2.read())

            post.author_track_waveform_base.save('author_track.png', base)
            post.author_track_waveform_cover.save('author_track_cover.png', cover)

            post.save()
            print(f'{waveform_base} saved')
