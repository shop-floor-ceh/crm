from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from shop_floor.settings import BASE_DIR
from account.forms import CreateUserForm, LoginUserForm, NotificationSettingForm
from account.models import Account, Notification
from account.utils import token_generator

import os


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
    return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'login.html'), context)


# def profile_plug(request):
#     return redirect('/')


def registration(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect('/profile')
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user_form.is_active = False
            user = user_form.save()
            Notification.objects.create(user=user, telegram=False, mail=False, vk=False)

            user_id = urlsafe_base64_encode(force_bytes(user.username))
            domain = get_current_site(request).domain
            relative = reverse('activate', kwargs={'user_id': user_id, 'token': token_generator.make_token(user)})
            activate_url = f'http://{domain}{relative}'

            email_subject = 'Подтверждение почты'
            email_body = f'Привет, {user.username}, это активация аккаунта, перейди по ссылке чтобы ' \
                         f'верефицировать свой аккаунт\n{activate_url}'
            email = EmailMessage(email_subject, email_body, 'noreply@semycolon.com', [user.email], )
            email.send(fail_silently=False)

            messages.success(request, 'Подтвердите свою почту и войдите')
            return redirect('/login')
    user_form = CreateUserForm()
    context = {'form': user_form}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'registration.html'), context)


def logout_def(request):
    logout(request)
    return redirect('/')


def profile_page(request, username):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    user = Account.objects.get(username=username)
    user.photo.name = '/'.join(user.photo.name.split('/')[1:])
    context = {'user': user}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'profile.html'), context)


def settings_page(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    if request.method == 'POST':
        user = Account.objects.get(username=request.user.username)
        notify = Notification.objects.get(user=user)

        notify.telegram = True if 'telegram' in request.POST else False
        notify.mail = True if 'mail' in request.POST else False
        notify.save()
        messages.success(request, 'Успешно сохранено')
        return redirect('/settings')
    user = Account.objects.get(username=request.user.username)
    user.photo.name = '/'.join(user.photo.name.split('/')[1:])
    notification = Notification.objects.get(user=user)
    notify_form = NotificationSettingForm()
    context = {'notification': notification, 'user': user, 'notify_form':notify_form}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'settings.html'), context)


def verification_email(request, user_id, token):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect('/profile')
    try:
        username = force_text(urlsafe_base64_decode(user_id))
        user = Account.objects.get(username=username)
        if token_generator.check_token(user, token) and user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Аккаунт успешко активирован')
            return redirect('/login')
        messages.success(request, 'Аккаунт по каким-то причинам не был активирован')
        return redirect('/login')
    except:
        pass
    return redirect('/login')
