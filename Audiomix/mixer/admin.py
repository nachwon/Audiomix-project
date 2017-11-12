from django.contrib import admin

from mixer.models import Post, Commit

admin.site.register(Post)
admin.site.register(Commit)
