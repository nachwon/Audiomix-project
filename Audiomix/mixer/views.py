from django.shortcuts import render
from pydub import AudioSegment
from mixer.models import Post


def mixer(request):
    return render(request, 'mixer.html')
