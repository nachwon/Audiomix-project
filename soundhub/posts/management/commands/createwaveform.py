import re
import os

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage as storage
from pydub.exceptions import CouldntDecodeError

from posts.models import Post, CommentTrack
from utils.pywave import Waveform


class Command(BaseCommand):
    help = 'Creates waveform image from an audio file source'

    def add_arguments(self, parser):
        parser.add_argument('--post', dest='post', action='store_true',
                            help='draws waveform of post audio tracks')
        parser.add_argument('--comment', dest='comment', action='store_true',
                            help='draws waveform of comment audio tracks')

    def handle(self, *args, **options):

        url_parser = re.compile(r".*?/media/(.*)[?].*")
        error_count = 0
        error_list = []

        if options['post']:
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
                    error_obj = f'user_{post.author.pk}/Post_{post.pk}'
                    print(f'CoudntDecodeError raised!: ' + error_obj)
                    error_count += 1
                    error_list.append(error_obj)
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

                os.remove(waveform_base)
                os.remove(waveform_cover)

                print(f'{waveform_base} saved')

        elif options['comment']:
            comments = CommentTrack.objects.all()
            for comment in comments:
                audio_dir = comment.comment_track.url
                audio_file = url_parser.search(audio_dir).group(1)
                try:
                    cover_png = comment.comment_track_waveform_cover.url
                    cover_png_parsed = url_parser.search(cover_png).group(1)
                    print(f'{cover_png_parsed} exists')
                    continue
                except ValueError:
                    audio_track = storage.open(audio_file, 'r')

                try:
                    waveform = Waveform(audio_track, audio_track.name)
                except CouldntDecodeError:
                    error_obj = f'user_{comment.author.pk}/Post_{comment.post.pk}/comment_tracks/comment_{comment.pk}'
                    print(f'CoudntDecodeError raised!: ' + error_obj)
                    error_count += 1
                    error_list.append(error_obj)
                    continue

                waveform_base = waveform.save()
                waveform_cover = waveform.change_color(waveform_base)

                with open(waveform_base, 'rb') as f1:
                    base = ContentFile(f1.read())

                with open(waveform_cover, 'rb') as f2:
                    cover = ContentFile(f2.read())

                comment.comment_track_waveform_base.save('comment_track.png', base)
                comment.comment_track_waveform_cover.save('comment_track_cover.png', cover)

                comment.save()

                os.remove(waveform_base)
                os.remove(waveform_cover)

                print(f'{waveform_base} saved')
        print('')
        print('Creating waveforms task finished')
        print('Errors occurred: ' + str(error_count))
        print('Errors list: ')
        for error in error_list:
            print(error)
