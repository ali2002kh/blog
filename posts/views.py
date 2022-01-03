from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from posts.forms import addCommentForm
from posts.models import Comment, Post
from django.core.paginator import Paginator

def posts_list(request):
    last_recent_posts = []
    most_visited_posts = []
    last_recent_posts = Post.objects.all().order_by('-date')[:5]
    most_visited_posts = Post.objects.all().order_by('-visited')[:5]
    
    base = 'date'
    sort = 'des'
    
    if 'base' in request.session:
        base = request.session['base']
        
    if 'sort' in request.session:
        sort = request.session['sort']
    
    if 'base' in request.POST:
        if not request.POST['base'] == '':
            base = request.POST['base']
            request.session['base'] = base
            
    if 'sort' in request.POST:
        if not request.POST['sort'] == '':
            sort = request.POST['sort']
            request.session['sort'] = sort
            
    sortedPosts = []
    
    if base == 'date':
        if sort == 'des':
            sortedPosts = Post.objects.all().order_by('-date')
        else:
            sortedPosts = Post.objects.all().order_by('date')
    elif base == 'comment':
        if sort == 'des':
            sortedPosts = Post.objects.all().order_by('-noc')
        else:
            sortedPosts = Post.objects.all().order_by('noc')
    else:
        if sort == 'des':
            sortedPosts = Post.objects.all().order_by('-visited')
        else:
            sortedPosts = Post.objects.all().order_by('visited')
    
    context = {
        'most_visited_posts': most_visited_posts,
        'last_recent_posts': last_recent_posts,
        'posts' : sortedPosts
    }          
            
    if 'filter' in request.POST:
        valid_date = True
        try:
            start = request.POST['start']
            end = request.POST['end']
        except:
            valid_date = False
        else:
            context['start'] = start
            context['end'] = end
                       
        if valid_date:
            sortedPosts = sortedPosts.filter(date__range=[start, end])
            
    if 'searching' in request.POST:
        searchedWord = request.POST['search']
        sortedPosts = Post.objects.filter(Q(title__icontains=searchedWord) |
                                          Q(body__icontains=searchedWord))
    
    paginator_list = Paginator(sortedPosts, 3)
    firstPage = request.GET.get('page') 
    context['posts'] = paginator_list.get_page(firstPage) 
    
    return render(request, 'posts/posts_list.html', context=context)


def post_detail(request, post_id):
    last_recent_posts = []
    most_visited_posts = []
    last_recent_posts = Post.objects.all().order_by('-date')[:5]
    most_visited_posts = Post.objects.all().order_by('-visited')[:5]
    post = Post.objects.get(id=post_id)
    post.visited = post.visited + 1
    post.save()
    comments = Comment.objects.all().filter(Q(is_confirmed=True) & Q(parent=None) & Q(post=post))
    context = {
        'most_visited_posts': most_visited_posts,
        'last_recent_posts': last_recent_posts,
        'post' : post,
        'comments': comments
    }    
    return render(request, 'posts/post_detail.html', context)


def addComment(request, post_id):
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/posts/'+str(post_id)) 
    post = Post.objects.get(id=post_id)
    form = addCommentForm(request.POST)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.author = user
        instance.post = post
        if user.id == post.author.id:
            instance.is_confirmed = True
        instance.save()
    return redirect('posts:detail', post_id)   


def replyComment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/posts/'+str(post.id)) 
    form = addCommentForm(request.POST)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.author = user
        instance.post = post
        instance.parent = comment
        if user.id == post.author.id:
            instance.is_confirmed = True
        instance.save()
    return redirect('posts:detail', post.id)


