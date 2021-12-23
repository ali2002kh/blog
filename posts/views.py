from django.shortcuts import render
from posts.models import Post

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    last_recent_posts = []
    most_visited_posts = []
    promoted_posts = []
    last_recent_posts = posts[:5]
    most_visited_posts = posts.order_by('-visited')[:5]
    promoted_posts = posts.filter(promote=True)
    context = {
        'posts': posts,
        'most_visited_posts': most_visited_posts,
        'promoted_posts': promoted_posts,
        'last_recent_posts': last_recent_posts
    }
    return render(request, 'posts/posts_list.html', context=context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})