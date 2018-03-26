import re

from django.core.files.storage import default_storage as storage
from django.core.management import BaseCommand

from posts.models import Post


class Command(BaseCommand):
    help = "saves master track"

    def add_arguments(self, parser):
        parser.add_argument('--default', dest='default', action='store_true',
                          help='saves the author track to master track')

    def handle(self, *args, **options):
        url_parser = re.compile(r".*?/media/(.*)[?].*")

        if options['default']:
            posts = Post.objects.all()

            for post in posts:
                try:
                    post.master_track.url
                    print(f'Post_{post.pk}: Master track already exists. Skipping the process.')

                except ValueError:
                    author_track_dir = post.author_track.url
                    author_track_file = url_parser.search(author_track_dir).group(1)
                    author_track = storage.open(author_track_file, 'r')

                    author_track_waveform_base = post.author_track_waveform_base.url
                    waveform_base_dir = url_parser.search(author_track_waveform_base).group(1)
                    waveform_base = storage.open(waveform_base_dir, 'r')

                    author_track_waveform_cover = post.author_track_waveform_cover.url
                    waveform_cover_dir = url_parser.search(author_track_waveform_cover).group(1)
                    waveform_cover = storage.open(waveform_cover_dir, 'r')

                    post.master_track.save('master_track.mp3', author_track)
                    post.master_track_waveform_base.save('master_track_waveform_base.png', waveform_base)
                    post.master_track_waveform_cover.save('master_track_waveform_cover.png', waveform_cover)

                    print(f'Post_{post.pk}: Successfully saved author track to master track.')
                break
