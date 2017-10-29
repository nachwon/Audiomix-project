from django.shortcuts import render
from pydub import AudioSegment
from mixer.models import Audio


def mixer(request):
    if request.method == 'POST':
        track_1 = AudioSegment.from_mp3(request.FILES['track-1'])
        track_2 = AudioSegment.from_mp3(request.FILES['track-2'])
        output = track_1.overlay(track_2)
        output.export('media/mixed.mp3')
        # Audio.objects.create(track=output)
        # context = {
        #     'audio': audio,
        # }
    return render(request, 'mixer.html')
