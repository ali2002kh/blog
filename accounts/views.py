from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request,user)
            request.session['login'] = True
            return redirect('home')  
        else:
            pass       
    return render(request, 'accounts/signup.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # login(request, user)
            request.session['login'] = True
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home') 
        
    return render(request, 'accounts/login.html')  


def logout_view(request):
    # logout(request)
    request.session['login'] = False
    return redirect('home')
