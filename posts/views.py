from django.db.models.query_utils import Q
from django.shortcuts import render
from posts.models import Post
from django.core.paginator import Paginator

def posts_list(request):
    last_recent_posts = []
    most_visited_posts = []
    last_recent_posts = Post.objects.all().order_by('-date')[:5]
    most_visited_posts = Post.objects.all().order_by('-visited')[:5]
    
    base = 'date'
    sort = 'des'
    
    if 'base' in request.POST:
        if not request.POST['base'] == '':
            base = request.POST['base']
            
    if 'sort' in request.POST:
        if not request.POST['sort'] == '':
            sort = request.POST['sort']
            
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
            end = request.POST['e_date']
        except:
            valid_date = False
        else:
            context['start'] = start
            context['end'] = end
                       
        if valid_date:
            context['posts'] = sortedPosts.filter(date__range=[start, end])
            
    if 'search' in request.POST:
        searchedWord = request.POST['search']
        sortedPosts = Post.objects.filter(Q(title__icontains=searchedWord) |
                                          Q(body__icontains=searchedWord))
    
    paginator_list = Paginator(sortedPosts, 5)
    firstPage = request.GET.get('page1') 
    context['posts'] = paginator_list.get_page(firstPage) 
    
    return render(request, 'posts/posts_list.html', context=context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})

