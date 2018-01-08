from django.contrib.auth import get_user_model
from django.shortcuts import render

from posts.models import Post

User = get_user_model()


def index(request):
    context = {
        "pop_users": User.objects.order_by('-total_liked')[:15],
        "pop_posts": Post.objects.order_by('-num_liked')[:15]
    }
    return render(request, 'index.html', context)