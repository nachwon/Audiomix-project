from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from posts.models import Post
from users.forms import SignInForm

User = get_user_model()


def index(request):
    if request.user.is_anonymous:
        context = {
            "pop_posts": Post.objects.order_by('-num_liked')[:8],
            "sign_in": SignInForm()
        }
        return render(request, 'index.html', context)

    else:
        return redirect('views:home')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    else:
        return redirect('views:index')
