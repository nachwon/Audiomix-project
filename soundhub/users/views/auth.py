from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.shortcuts import redirect, render

from users.forms import SignInForm, SignUpForm
from utils.facebook import get_facebook_user_info
from utils.google import get_google_user_info

User = get_user_model()


def sign_up_index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('views:home')
        context = {
            "google_client_id": settings.GOOGLE_CLIENT_ID,
            "sign_in": SignInForm(),
        }
        return render(request, 'sign/signup-index.html', context)


def sign_up(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('views:home')
        form = SignUpForm()
        fields = list(form)
        context = {
            "required": fields[:4],
            "genre": fields[4],
            "instrument": fields[5],
            "sign_in": SignInForm(),
        }
        return render(request, 'sign/signup.html', context)

    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            # m2m 관계 필드 폼으로 받아서 저장
            form.save_m2m()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('views:home')
        else:
            form = SignUpForm(request.POST)
            fields = list(form)
            context = {
                "required": fields[:4],
                "genre": fields[4],
                "instrument": fields[5],
                "sign_in": SignInForm(),
            }
            return render(request, 'sign/signup.html', context)


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('views:home')

    else:
        form = SignInForm()

    context = {
        "sign_in": form,
        "google_client_id": settings.GOOGLE_CLIENT_ID,
    }
    return render(request, 'sign/signin.html', context)


def facebook_login(request):
    user_info = get_facebook_user_info(request)
    fb_id = user_info.get('id')

    # 유저 인증 및 로그인
    # authenticate 를 거치면 user.backend 속성에 인증에 사용된 벡엔드가 부여됨.
    user = authenticate(oauth_id=fb_id, user_type='F')

    if user:
        pass

    else:
        fb_username = f'fb_{fb_id}'
        email = user_info.get('email', fb_username)
        nickname = user_info.get('name', fb_username)
        user = User.objects.create(
            email=email,
            nickname=nickname,
            oauth_id=fb_id,
            user_type='F'
        )

    login(request, user, backend='users.backends.OAuthBackend')
    return redirect('views:home')


def google_login(request):
    user_info = get_google_user_info(request)
    gg_id = user_info.get('id')

    user = authenticate(oauth_id=gg_id, user_type='G')

    if user:
        pass

    else:
        gg_username = f'gg_{gg_id}'
        email = user_info.get('email', gg_username)
        nickname = user_info.get('name', gg_username)

        user = User.objects.create(
            email=email,
            nickname=nickname,
            oauth_id=gg_id,
            user_type='G'
        )
    login(request, user, backend='users.backends.OAuthBackend')
    return redirect('views:home')


def sign_out(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
    return redirect('views:index')
