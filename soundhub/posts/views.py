import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from posts.models import Post, PostLike


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    guitar = post.comment_tracks.filter(is_mixed=False).filter(instrument__name="Guitar")
    bass = post.comment_tracks.filter(is_mixed=False).filter(instrument__name="Bass")
    drums = post.comment_tracks.filter(is_mixed=False).filter(instrument__name="Drums")
    keys = post.comment_tracks.filter(is_mixed=False).filter(instrument__name="Keyboard")
    vocal = post.comment_tracks.filter(is_mixed=False).filter(instrument__name="Vocal")
    others = post.comment_tracks.filter(is_mixed=False).filter(instrument__name="Others")

    context = {
        'post': post,
        'mixed': post.mixed_tracks.all(),
        'comments': post.comment_tracks.filter(is_mixed=False),
        'guitar': guitar,
        'bass': bass,
        'drums': drums,
        'keys': keys,
        'vocal': vocal,
        'others': others

    }
    return render(request, 'post-detail/post-detail.html', context=context)


@login_required
@require_POST
def like_toggle(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)

    if user.liked_posts.filter(id=post.pk).exists():
        PostLike.objects.get(author=user, post=post).delete()

    else:
        PostLike.objects.create(author=user, post=post)

    response = {
        "count": post.liked.count()
    }
    json_response = json.dumps(response)
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    return HttpResponse(json_response, content_type=header["Content-Type"],
                        charset=header["charset"])
