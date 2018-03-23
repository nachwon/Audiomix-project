from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--post', dest='post', action='store_true', help='draws waveform of post audio track')

    def handle(self, *args, **options):
        if options['post']:
            print(args)
            print("hello")

        print("hi")
