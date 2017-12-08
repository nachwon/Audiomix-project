from django.contrib import admin

from posts.models import Post, CommentTrack, PostLike

admin.site.register(Post)
admin.site.register(CommentTrack)
admin.site.register(PostLike)

