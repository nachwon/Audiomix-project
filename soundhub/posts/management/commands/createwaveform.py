from django.core.management.base import BaseCommand

from utils.pywave import Waveform


class Command(BaseCommand):
    help = 'Creates waveform image from an audio file source'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            help='Draw waveform for all the tracks.'
        )

    def handle(self, *args, **options):
        filename = options.get('filename', False)

        if filename:
            waveform = Waveform(filename)
            waveform_base = waveform.save()
