from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from posts.models import Post
from users.forms import SignInForm, SignUpForm

User = get_user_model()


def index(request):
    if request.user.is_anonymous:
        context = {
            "pop_users": User.objects.order_by('-total_liked')[:8],
            "pop_posts": Post.objects.order_by('-num_liked')[:8],
            "recent_posts": Post.objects.order_by('-created_date')[:8],
            "sign_in": SignInForm(),
        }
        return render(request, 'index.html', context)

    else:
        return redirect('views:home')


def home(request):
    if request.user.is_authenticated:
        context = {
            "followings": request.user.following,
        }
        return render(request, 'home/home.html', context)
    else:
        return redirect('views:index')
