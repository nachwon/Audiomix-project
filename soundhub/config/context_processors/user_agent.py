def http_user_agent(request):
    chrome = 'Chrome'
    firefox = "Firefox"
    user_agent = request.META['HTTP_USER_AGENT']

    if chrome in user_agent:
        user_agent = chrome
    elif firefox in user_agent:
        user_agent = firefox

    return {'user_agent': user_agent}
