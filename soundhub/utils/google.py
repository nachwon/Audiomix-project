import requests
from django.conf import settings
from django.urls import reverse


def get_google_user_info(request):
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET

    code = request.GET.get('code')
    redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse('views:user:google-login')}"
    print(redirect_uri)
    params_access_token = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    url_access_token = 'https://www.googleapis.com/oauth2/v4/token'

    response = requests.post(url_access_token, params=params_access_token)

    token_data = response.json()
    access_token = token_data.get('access_token')
    user_info_request_uri = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Bearer': access_token}
    params = {
        'access_token': access_token
    }
    user_info = requests.get(user_info_request_uri, headers=headers, params=params)
    return user_info
