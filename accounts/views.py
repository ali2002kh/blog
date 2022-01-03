from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

def signup_view(request):
    message = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['login'] = user.id
            return redirect('home')  
        else:
            message = 'نام کاربری یا رمز معتبر نیست' 
    return render(request, 'accounts/signup.html', {'message': message})


def login_view(request):
    message = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            request.session['login'] = form.get_user().id
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home') 
        else:
            message = 'نام کاربری یا رمز عبور اشتباه است' 
    return render(request, 'accounts/login.html', {'message': message})  


def logout_view(request):
    del request.session['login']
    return redirect('home')
