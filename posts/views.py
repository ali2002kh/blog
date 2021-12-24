from django.shortcuts import redirect, render
from posts.models import Post
from posts.forms import CreatePostForm

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

def post_create(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.author = request.user
            instance.save()
            return redirect('home')
        
    else:
        form = CreatePostForm()   
    
    return render(request,'posts/create.html', {'form':form})