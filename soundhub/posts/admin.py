from django.contrib import admin

from posts.models import Post, CommentTrack, PostLike, MixedTrack

admin.site.register(Post)
admin.site.register(CommentTrack)
admin.site.register(PostLike)
admin.site.register(MixedTrack)
