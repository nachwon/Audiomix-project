from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.forms import SignUpForm, SignInForm
from utils.facebook import get_facebook_user_info

User = get_user_model()


def sign_up(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('views:home')
        form = SignUpForm()
        fields = list(form)
        context = {
            "required": fields[:4],
            "more_info": fields[4:]
        }
        return render(request, 'sign/signup.html', context)

    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('views:home')


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
    }
    return render(request, 'sign/signin.html', context)


def facebook_login(request):
    user_info = get_facebook_user_info(request)
    fb_id = user_info.get('id')

    # 유저 인증 및 로그인
    # authenticate 를 거치면 user.backend 속성에 인증에 사용된 벡엔드가 부여됨.
    user = authenticate(fb_id=fb_id)
    # 여러개의 인증 벡엔드 사용 중일 경우 user.backend 속성으로 어떤 벡엔드로 인증되었는지 알려주어야 함.
    login(request, user, backend=user.backend)
    return redirect('views:home')


def sign_out(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
    return redirect('views:index')


def user_detail(request, pk):
    if request.method == 'GET':
        user = User.objects.get(pk=pk)

        context = {
            "user": user,
        }
        return render(request, 'profile/profile.html', context)
