from django.contrib.auth import get_user_model
from django.shortcuts import render

from posts.models import Post

User = get_user_model()


def index(request):
    context = {
        "pop_posts": Post.objects.order_by('-num_liked')[:10]
    }
    return render(request, 'index.html', context)
