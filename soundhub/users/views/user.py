import json
from itertools import chain

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from posts.models import Post, PostLike
from users.forms import SignInForm
from users.models import Relationship


User = get_user_model()


def user_detail(request, pk):
    user_exists = User.objects.all().filter(pk=pk).exists()

    if request.method == 'GET' and user_exists:
        user = User.objects.get(pk=pk)

        user_posts = user.post_set.all()[:5]
        user_comments = user.commenttrack_set.all()[:5]
        all_tracks = list(chain(user_posts, user_comments))

        context = {
            "sign_in": SignInForm,
            "user": user,
            "all_tracks": all_tracks,
        }
        return render(request, 'profile/profile.html', context)

    else:
        context = {
            "status_code": 404,
            "message": "Not Found!"
        }
        return render(request, 'error.html', context, status=404)


def follow_toggle(request, pk):
    from_user = request.user
    to_user = User.objects.get(pk=pk)

    if request.method == 'GET' and request.user.is_authenticated:
        response = Relationship.objects \
            .filter(from_user_id=from_user.pk) \
            .filter(to_user_id=to_user.pk) \
            .exists()
        return HttpResponse(response)

    elif request.method == 'POST' and request.user.is_authenticated:
        if Relationship.objects\
                .filter(from_user_id=from_user.pk)\
                .filter(to_user_id=to_user.pk)\
                .exists():

            relation = Relationship.objects.get(
                from_user_id=from_user.pk,
                to_user_id=to_user.pk
            )
            relation.delete()
            response = {
                "status": 204
            }

        else:
            Relationship.objects.create(
                from_user_id=from_user.pk,
                to_user_id=to_user.pk
            )
            response = {
                "status": 201
            }

        response["count"] = f"{to_user.followers.count()}"
        json_response = json.dumps(response)
        header = {
            "Content-Type": "application/json",
            "charset": "utf-8"
        }

        return HttpResponse(json_response,
                            content_type=header["Content-Type"],
                            charset=header["charset"],
                            status=response["status"])
