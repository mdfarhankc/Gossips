from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('index')
