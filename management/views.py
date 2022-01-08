from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from posts.forms import CreatePostForm
from posts.models import Comment, Post


def index(request):
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/management/') 
    posts = Post.objects.all().filter(author=user.id).order_by('-date')
    return render(request, 'management/index.html', {'posts': posts, 'user': user})


def create(request):
    message = None
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/management/create') 
    if request.method == 'POST':
        form = CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.author = user
            instance.save()
            return redirect('management:index')   
        else:
            message = 'اطلاعات پست را درست وارد کنید' 
    return render(request,'management/create.html', {'message': message})

    
def delete(request, post_id):
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/management') 
    try:
        post = Post.objects.get(id=post_id)
    except:
        return render(request,'management/post404.html', {'post_id' : post_id})
    if user.id == post.author.id:
        post.delete()
    return redirect('management:index')


def comments(request, post_id):
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/management/'+str(post_id)+'/comments') 
    try:
        post = Post.objects.get(id=post_id)
    except:
        return render(request,'management/post404.html', {'post_id' : post_id})
    if user.id == post.author.id:
        comments = Comment.objects.all().filter(Q(post=post) & Q(is_confirmed=False))
        return render(request, 'management/comments.html', {'comments': comments})
    return redirect('management:index')

def confirm(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return render(request,'management/comment404.html', {'comment_id' : comment_id})
    post = comment.post
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/management/'+str(post.id)+'/comments') 
    if comment.post.author.id == user.id:
        comment.is_confirmed = True
        post.noc = post.noc + 1
        post.save()
        comment.save()
    return redirect('management:comments', post.id)


def reject(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return render(request,'management/comment404.html', {'comment_id' : comment_id})
    post = comment.post
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/management/'+str(post.id)+'/comments') 
    if comment.post.author.id == user.id:
        comment.delete()
    return redirect('management:comments', post.id)
    

def edit(request, post_id):
    message = None
    try:
        user = User.objects.get(id=request.session['login'])
    except:
        return redirect('/accounts/login/?next=/management/'+str(post_id)+'/edit')
    try:
        post = Post.objects.get(id=post_id)
    except:
        return render(request,'management/post404.html', {'post_id' : post_id})
    if user  != post.author:
        return render(request,'management/403.html', {'post_id' : post_id})
    if request.method == 'POST':
        form = CreatePostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return redirect('management:index')   
        else:
            message = 'اطلاعات پست را درست وارد کنید' 
    return render(request,'management/edit.html', {'message': message, 'post':post})