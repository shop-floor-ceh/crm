from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import login, logout
from account.models import Account


def profile_page(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    user = Account.objects.get(username=request.user.username)
    user.photo.name = '/'.join(user.photo.name.split('/')[1:])
    context = {'user': user}
    return render(request, 'profile.html', context)


# def profile_plug(request):
#     return redirect('/')


def authorization(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect('/profile')
    form = LoginUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/profile')
        else:
            messages.error(request, 'Такого пользователя не найдено')
    return render(request, 'login.html', context)


def registration(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect('/profile')
    form = CreateUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile')
    return render(request, 'registration.html', context)


def logout_def(request):
    logout(request)
    return redirect('/')
