from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

from mixer.serializer import PostSerializer, CommitSerializer
from .models import Post, Commit


@csrf_exempt
def post_detail(request, pk):
    if request.method == 'GET':
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK, json_dumps_params={'indent': 4})

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        data =JSONParser().parse(request)
        serializer = CommitSerializer(data=data)
        if serializer.is_valid():
            serializer.save(post=post)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

