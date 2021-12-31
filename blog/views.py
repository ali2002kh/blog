from django.core.paginator import Paginator
from django.shortcuts import render
from posts.models import Post

def home(request):
    posts = Post.objects.all().order_by('-date')
    most_visited_posts = []
    promoted_posts = []
    last_recent_posts = []
    last_recent_posts = posts[:5]
    most_visited_posts = posts.order_by('-visited')[:5]
    promoted_posts = posts.filter(promote=True)
    context = {
        'posts': posts,
        'most_visited_posts': most_visited_posts,
        'promoted_posts': promoted_posts,
        'last_recent_posts': last_recent_posts
    }
    
    paginator_main = Paginator(posts, 5)
    firstPage = request.GET.get('page1') 
    context['posts'] = paginator_main.get_page(firstPage) 
    
    return render(request, 'home/home.html', context=context)