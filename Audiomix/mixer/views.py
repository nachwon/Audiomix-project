from django.http import JsonResponse
from django.shortcuts import render
from pydub import AudioSegment

from mixer.serializer import PostSerializer
from .models import Post


def post_detail(request, pk):
    if request.method == 'GET':
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
