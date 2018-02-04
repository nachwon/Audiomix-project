import sys

import os

from django.conf import settings
from pydub import AudioSegment
from PIL import Image, ImageDraw


class Waveform(object):
    bar_count = 150
    db_ceiling = 60

    def __init__(self, file, filename):
        self.filename = filename
        self.file = file

        audio_file = AudioSegment.from_file(
            self.file, self.filename.split('.')[-1])

        self.peaks = self._calculate_peaks(audio_file)

    def _calculate_peaks(self, audio_file):
        """ Returns a list of audio level peaks """
        chunk_length = len(audio_file) / self.bar_count

        loudness_of_chunks = [
            audio_file[i * chunk_length: (i + 1) * chunk_length].rms
            for i in range(self.bar_count)]

        max_rms = max(loudness_of_chunks) * 1.00

        return [int((loudness / max_rms) * self.db_ceiling)
                for loudness in loudness_of_chunks]

    def _get_bar_image(self, size, fill):
        """ Returns an image of a bar. """
        width, height = size
        bar = Image.new('RGBA', size, fill)

        # end = Image.new('RGBA', (width, 2), fill)
        # print(bar)
        # draw = ImageDraw.Draw(end)
        # draw.point([(0, 0), (3, 0)], fill='#c1c1c1')
        # draw.point([(0, 1), (3, 1), (1, 0), (2, 0)], fill='#333533')

        # bar.paste(end, (0, 0))
        # bar.paste(end.rotate(180), (0, height - 2))
        return bar

    def _generate_waveform_image(self):
        """ Returns the full waveform image """
        bar_width = 3
        px_between_bars = 1
        offset_left = 4
        offset_top = 4

        width = ((bar_width + px_between_bars) * self.bar_count) + (offset_left * 2)
        height = (self.db_ceiling + offset_top) * 2

        im = Image.new('RGBA', (width, height), '#ffffff00')
        for index, value in enumerate(self.peaks, start=0):
            column = index * (bar_width + px_between_bars) + offset_left
            upper_endpoint = (self.db_ceiling - value) + offset_top

            im.paste(self._get_bar_image((bar_width, value * 2), '#333533'),
                     (column, upper_endpoint))

        return im

    def save(self):
        """ Save the waveform as an image """
        png_filename = self.filename.replace(
            self.filename.split('.')[-1], 'png')

        media_dir = os.path.join(settings.MEDIA_ROOT, png_filename)

        directory = os.path.dirname(media_dir)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(media_dir, 'wb') as imfile:
            self._generate_waveform_image().save(imfile, 'PNG')
        return media_dir

    @staticmethod
    def change_color(base_png):
        im = Image.open(base_png)
        newimdata = []
        black1 = (51, 53, 51, 255)
        yellow1 = (226, 176, 38, 255)
        blank = (255, 255, 255, 0)
        for color in im.getdata():
            if color == black1:
                newimdata.append(yellow1)
            else:
                newimdata.append(blank)
        newim = Image.new(im.mode, im.size)
        newim.putdata(newimdata)

        out_dir = base_png.replace('.' + base_png.split('.')[-1], '_cover.png')
        newim.save(out_dir)
        return out_dir


if __name__ == '__main__':
    filename = sys.argv[1]
    waveform = Waveform(filename)
    base = waveform.save()
    waveform.change_color(base)
