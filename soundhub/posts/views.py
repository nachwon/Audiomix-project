from django.http import HttpResponse

from posts.models import Post, PostLike


def like_toggle(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)

    if request.method == "POST" and request.user.is_authenticated:
        if user.liked_posts.all().filter(id=post.pk).exists():
            PostLike.objects.get(author=user, post=post).delete()
        else:
            PostLike.objects.create(author=user, post=post)

        return HttpResponse(status=200)