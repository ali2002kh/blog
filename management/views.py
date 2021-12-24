from django.shortcuts import redirect, render
from posts.forms import CreatePostForm
from posts.models import Post

def index(request):
    user = request.user
    posts = Post.objects.all().filter(author=user.id).order_by('-date')
    return render(request, 'management/index.html', {'posts': posts, 'user': user})

def create(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.author = request.user
            instance.save()
            return redirect('management:index')
        
    else:
        form = CreatePostForm()   
    
    return render(request,'management/create.html', {'form':form})


def edit(request, post_id):
    if request.method == 'POST':
        pass
    else:
        post = Post.objects.get(id=post_id)

    return render(request, 'management/edit.html', {'posts': post})

def delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('management:index')