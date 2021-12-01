from django.shortcuts import render
from . import models

def posts_list(request):
    posts = models.post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})


def post_detail(request,slug):
    post = models.post.objects.get(slug=slug)
    return render(request, 'posts/post_detail.html', {'post': post})
    