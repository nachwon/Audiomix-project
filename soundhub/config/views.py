from django.shortcuts import redirect, render


def redirect_to_home(request):
    return redirect('home:index')


def page_not_found(request):
    return render(request, '404.html')
