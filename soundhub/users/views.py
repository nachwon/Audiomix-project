from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)

    return render(request, 'home/home.html')
