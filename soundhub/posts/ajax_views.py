import django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from posts.models import CommentTrack, Post


class SendCommentTrack(View):

    def post(self, request, pk):
        comment = get_object_or_404(CommentTrack, pk=pk)
        response = HttpResponse()
        audio_file = comment.comment_track.file

        response.write(audio_file.read())

        user_agent = request.META["HTTP_USER_AGENT"]
        if "Firefox" in user_agent:
            response['Content-Type'] = "audio/mpeg"
        elif "Chrome" in user_agent:
            response['Content-Type'] = "audio/mp3"

        response['Content-Length'] = audio_file.size

        return response


class SendAuthorTrack(View):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        response = HttpResponse()
        audio_file = post.author_track.file

        response.write(audio_file.read())

        user_agent = request.META["HTTP_USER_AGENT"]
        if "Firefox" in user_agent:
            response['Content-Type'] = "audio/mpeg"
        elif "Chrome" in user_agent:
            response['Content-Type'] = "audio/mp3"

        response['Content-Length'] = audio_file.size

        return response
