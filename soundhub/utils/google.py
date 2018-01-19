from django.conf import settings
from django.urls import reverse


def get_google_user_info(request):
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET

    code = request.GET.get('code')
    redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse('views:user:google-login')}"
    params_access_token = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    url_access_token = 'https://www.googleapis.com/oauth2/v4/token'
