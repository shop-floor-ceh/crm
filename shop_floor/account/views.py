from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm
from django.contrib.auth import login, logout


def profile_page(request):
    return render(request, 'profile.html')


def authorization(request):
    form = LoginUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            return redirect('register')
    return render(request, 'login.html', context)


def registration(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    return render(request, 'registration.html', context)


def logout_def(request):
    logout(request)
    return redirect('/')
