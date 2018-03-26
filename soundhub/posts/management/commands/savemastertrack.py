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
        saved_count = 0
        skipped_count = 0
        error_count = 0

        if options['default']:
            posts = Post.objects.all()

            for post in posts:
                try:
                    post.author_track_waveform_base.url
                    post.author_track_waveform_cover.url
                except ValueError:
                    print(f'Post_{post.pk}: Author track waveform is not saved. '
                          f'It seems that there is something wrong with the author track.')
                    error_count += 1
                    continue

                try:
                    post.master_track.url
                    print(f'Post_{post.pk}: Master track already exists. Skipping the process.')
                    skipped_count += 1

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
                    saved_count += 1

            print(f'Master track saved: {saved_count}')
            print(f'Process skipped: {skipped_count}')
            print(f'Error: {error_count}')
