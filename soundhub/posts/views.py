import json

from django.http import HttpResponse

from posts.models import Post, PostLike


def like_toggle(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)

    if request.method == "GET":
        is_liked = user.liked_posts.filter(id=post.pk).exists()
        print(is_liked)
        return HttpResponse(is_liked)

    elif request.method == "POST" and request.user.is_authenticated:
        if user.liked_posts.all().filter(id=post.pk).exists():
            PostLike.objects.get(author=user, post=post).delete()
            response = {
                "status": 204
            }

        else:
            PostLike.objects.create(author=user, post=post)
            response = {
                "status": 201
            }
        response["count"] = f"{post.liked.count()}"
        json_response = json.dumps(response)
        header = {
            "Content-Type": "application/json",
            "charset": "utf-8"
        }
        return HttpResponse(json_response, content_type=header["Content-Type"],
                            charset=header["charset"], status=response["status"])
