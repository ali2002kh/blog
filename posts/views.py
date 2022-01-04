from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from posts.forms import addCommentForm
from posts.models import Comment, Post
from django.core.paginator import Paginator
import datetime

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
    
    if 'clear_filter' in request.POST:
        if 'start' in request.session:
            del request.session['start']
        if 'end' in request.session:
            del request.session['end']  
        
    if 'clear_search' in request.POST:
        if 'search' in request.session:
            del request.session['search']  
            
    if 'filter' in request.POST:
        try:
            request.session['start'] = request.POST['start']
            request.session['end'] = request.POST['end']
        except:
            pass

    if 'start' in request.session and 'end' in request.session:
        is_valid = True
        try:
            datetime.datetime.strptime(request.session['start'], '%Y-%m-%d')
            datetime.datetime.strptime(request.session['end'], '%Y-%m-%d')
        except:
            is_valid = False
            if 'filter' in request.POST:
                context['error'] = "تاریخ شروع و پایان را انتخاب کنید"
            
        if is_valid:
            sortedPosts = sortedPosts.filter(date__range=[request.session['start'], request.session['end']])
                
            
            
    if 'searching' in request.POST:
        request.session['search'] = request.POST['search']
    
    if 'search' in request.session:
        sortedPosts = Post.objects.filter(Q(title__icontains=request.session['search']) |
                                          Q(body__icontains=request.session['search']))
    
    paginator_list = Paginator(sortedPosts, 3)
    firstPage = request.GET.get('page') 
    context['posts'] = paginator_list.get_page(firstPage) 
    
    return render(request, 'posts/posts_list.html', context=context)


def post_detail(request, post_id):
    last_recent_posts = []
    most_visited_posts = []
    last_recent_posts = Post.objects.all().order_by('-date')[:5]
    most_visited_posts = Post.objects.all().order_by('-visited')[:5]
    try:
        post = Post.objects.get(id=post_id)
    except:
        return render(request, 'posts/post404.html', {'post_id': post_id})
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
    try:
        post = Post.objects.get(id=post_id)
    except:
        return render(request, 'posts/post404.html', {'post_id': post_id})
    form = addCommentForm(request.POST)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.author = user
        instance.post = post
        if user.id == post.author.id:
            instance.is_confirmed = True
            post.noc = post.noc + 1
            post.save()
        instance.save()
    return redirect('posts:detail', post_id)   


def replyComment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return render(request,'posts/comment404.html', {'comment_id' : comment_id})
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
            post.noc = post.noc + 1
            post.save()
        instance.save()
    return redirect('posts:detail', post.id)


