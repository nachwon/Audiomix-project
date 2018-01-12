import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

User = get_user_model()


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)

    return redirect('views:home')


def facebook_login(request):
    app_id = settings.FB_APP_ID
    app_secret = settings.FB_SECRET_CODE

    # 토큰 요청
    code = request.GET['code']
    redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse('views:user:fb-login')}"
    url_access_token = "https://graph.facebook.com/v2.11/oauth/access_token"
    params_access_token = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "client_secret": app_secret,
        "code": code,
    }

    response = requests.get(url_access_token, params=params_access_token)

    # 토큰 검사
    access_token = response.json()['access_token']
    url_debug_token = 'https://graph.facebook.com/debug_token'
    params_debug_token = {
        "input_token": access_token,
        "access_token": f'{app_id}|{app_secret}'
    }

    debug_result = requests.get(url_debug_token, params=params_debug_token)

    # 토큰이 유효하면 유저 정보 요청
    if debug_result.json()['data']['is_valid'] is True:
        url_user_info = 'https://graph.facebook.com/me'
        user_info_fields = [
            'id',  # 아이디
            'first_name',  # 이름
            'last_name',  # 성
            'picture',  # 프로필 사진
            'email',  # 이메일
        ]
        params_user_info = {
            "fields": ','.join(user_info_fields),
            "access_token": access_token
        }
        result = requests.get(url_user_info, params=params_user_info)
        user_info = result.json()

        email = user_info.get('email')
        nickname = user_info.get('first_name') + ' ' + user_info.get('last_name')

        # 유저 생성
        obj, created = User.objects.get_or_create(
            email=email,
            nickname=nickname,
            user_type='Facebook'
        )

        # 유저 인증 및 로그인
        # authenticate 를 거치면 user.backend 속성에 인증에 사용된 벡엔드가 부여됨.
        user = authenticate(email=obj.email)
        # 여러개의 인증 벡엔드 사용 중일 경우 user.backend 속성으로 어떤 벡엔드로 인증되었는지 알려주어야 함.
        login(request, user, backend=user.backend)
    return redirect('views:home')


def sign_out(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
    return redirect('views:index')
