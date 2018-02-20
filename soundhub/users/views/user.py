import json

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views.decorators.http import require_GET, require_POST

from posts.models import PostLike
from users.forms import SignInForm
from users.models import Relationship


User = get_user_model()


# 유저 프로필 뷰
# 모든 사용자 접근 가능
# GET 요청만 허용
@require_GET
def user_detail(request, pk):
    # 프로필을 나타낼 유저 객체
    user = get_object_or_404(User, pk=pk)
    # 해당 유저가 좋아요한 포스트 목록
    liked_posts = PostLike.objects.filter(author=user).order_by('liked_date')[:5]
    # 해당 유저를 팔로우 하고 있는 유저 관계 목록
    followers = Relationship.objects.filter(to_user=user)[:14]
    # 해당 유저가 팔로잉 중인 유저 관계 목록
    followings = Relationship.objects.filter(from_user=user)[:14]

    context = {
        # 빈 로그인 폼
        "sign_in": SignInForm,
        "user": user,
        "liked_posts": liked_posts,
        "followers": followers,
        "followings": followings
    }
    return render(request, 'profile/profile.html', context)


# all_tracks ajax 요청 처리 뷰
# POST 요청만 허용
@require_POST
def get_tracks(request, pk):
    # 트랙 정보를 가져올 유저 객체
    user = get_object_or_404(User, pk=pk)

    # ajax 로부터 넘어온 페이지 카운터
    # 1에서 3까지의 숫자
    page = request.POST['counter']

    # 유저의 포스트 15개를 가져옴
    user_posts = user.post_set.all()[:15]
    # 5개씩 페이지네이션 적용
    paginator = Paginator(user_posts, 5)

    # ajax 로 받은 페이지 번호의 포스트 5개를 불러옴
    posts = paginator.page(page)

    context = {
        # ajax 요청으로 렌더링 된 템플릿이 request 객체를 사용할 수 있도록 그대로 넘겨줌
        "request": request,
        "user": user,
        # 전체 포스트 갯수를 파악하기 위해 15개 목록 전체의 쿼리셋을 넘겨줌
        "user_posts": user_posts,
        # 페이지네이션이 적용된 쿼리셋
        "posts": posts,
        # 페이지 번호를 다시 리턴해줌
        "page": page
    }

    # all-tracks.html 을 위의 context 를 가지고 렌더링 시킴
    html = loader.render_to_string(
        'profile/all-tracks.html',
        context
    )

    # 렌더링 된 html 을 json 형식으로 변환하여 ajax 요청의 response 로 돌려줌
    context = {
        "html": html
    }

    response = json.dumps(context)
    return HttpResponse(response)


# comments ajax 요청 처리 뷰
# POST 요청만 허용
def get_comments(request, pk):
    user = get_object_or_404(User, pk=pk)

    page = request.POST['counter']

    user_comments = user.commenttrack_set.all()[:15]
    print(user_comments)
    paginator = Paginator(user_comments, 5)

    comments = paginator.page(page)

    context = {
        # ajax 요청으로 렌더링 된 템플릿이 request 객체를 사용할 수 있도록 그대로 넘겨줌
        "request": request,
        "user": user,
        # 전체 커맨트 갯수를 파악하기 위해 15개 목록 전체의 쿼리셋을 넘겨줌
        "user_comments": user_comments,
        # 페이지네이션이 적용된 쿼리셋
        "comments": comments,
        # 페이지 번호를 다시 리턴해줌
        "page": page
    }

    html = loader.render_to_string(
        'profile/comments.html',
        context
    )

    # 렌더링 된 html 을 json 형식으로 변환하여 ajax 요청의 response 로 돌려줌
    context = {
        "html": html
    }

    response = json.dumps(context)
    return HttpResponse(response)









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
        if Relationship.objects \
                .filter(from_user_id=from_user.pk) \
                .filter(to_user_id=to_user.pk) \
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
