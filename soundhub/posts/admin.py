from django.contrib import admin

from posts.models import Post, CommentTrack

admin.site.register(Post)
admin.site.register(CommentTrack)
