from users.forms import SignInForm


def signin_form(request):
    return {'sign_in': SignInForm}