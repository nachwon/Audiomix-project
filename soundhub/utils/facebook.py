import requests
from django.conf import settings
from django.urls import reverse


def get_facebook_user_info(request):
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
            'name',  # 이름
            'picture',  # 프로필 사진
            'email',  # 이메일
        ]
        params_user_info = {
            "fields": ','.join(user_info_fields),
            "access_token": access_token
        }
        result = requests.get(url_user_info, params=params_user_info)
        user_info = result.json()

        return user_info
