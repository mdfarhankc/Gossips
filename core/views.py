from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from .forms import SignUpForm

def Index(request):
    return render(request, 'core/index.html')

def Signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('index')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('index')