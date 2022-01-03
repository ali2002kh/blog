from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from posts.forms import CreatePostForm
from posts.models import Comment, Post
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required

@login_required(login_url= "/accounts/login")  
def index(request):
    user = request.user
    posts = Post.objects.all().filter(author=user.id).order_by('-date')
    return render(request, 'management/index.html', {'posts': posts, 'user': user})

@login_required(login_url= "/accounts/login")  
def create(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.author = request.user
            instance.save()
            return redirect('management:index')   
    return render(request,'management/create.html')

class edit(UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'management/edit.html'
    
@login_required(login_url= "/accounts/login") 
def delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('management:index')

@login_required(login_url= "/accounts/login") 
def comments(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.all().filter(Q(post=post) & Q(is_confirmed=False))
    return render(request, 'management/comments.html', {'comments': comments})

@login_required(login_url= "/accounts/login") 
def confirm(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.is_confirmed = True
    post = comment.post
    post.noc = post.noc + 1
    post.save()
    comment.save()
    return redirect('management:comments', post.id)

@login_required(login_url= "/accounts/login") 
def reject(request, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return redirect('management:comments', Comment.objects.get(id=comment_id).post.id)
    