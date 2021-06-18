from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from shop_floor.settings import BASE_DIR
from account.forms import CreateUserForm, LoginUserForm
from account.models import Account, Notification, SocialNetworks
from account.utils import token_generator

import os


def profile_page(request, username):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    if request.method == 'POST':
        if 'update_user' in request.POST:
            user = Account.objects.get(username=request.user.username)
            if 'username' in request.POST:
                user.username = request.POST['username']
            if 'first_name' in request.POST:
                user.first_name = request.POST['first_name']
            if 'last_name' in request.POST:
                user.last_name = request.POST['last_name']
            if 'about_me' in request.POST:
                user.about_me = request.POST['about_me']
            if 'phone' in request.POST:
                user.phone = request.POST['phone']
            if 'photo' in request.FILES:
                user.photo = request.FILES['photo']
            try:
                user.save()
                messages.success(request, 'Успешно изменено')
                return redirect(f'/profile/{user.username}')
            except:
                messages.error(request, 'Что-то пошло не так')
                return redirect(f'/profile/{request.user.username}')

        elif 'add-network' in request.POST:
            user = Account.objects.get(username=request.user.username)
            network = SocialNetworks(user=request.user, network_name=request.POST['network_name'],
                                     link=request.POST['link'])
            network.save()
            messages.success(request, 'Успешно добавлено')
            return redirect(f'/profile/{user.username}')
        elif 'notify' in request.POST:
            user = Account.objects.get(username=request.user.username)
            notify = Notification.objects.get(user=user)
            notify.telegram = True if 'telegram' in request.POST else False
            notify.mail = True if 'mail' in request.POST else False
            notify.save()
            messages.success(request, 'Успешно сохранено')
            return redirect(f'/profile/{user.username}')
    user = Account.objects.get(username=username)
    networks = SocialNetworks.objects.filter(user=user)
    user.photo.name = '/'.join(user.photo.name.split('/')[1:])
    notification = Notification.objects.get(user=user)
    context = {
        'user': user,
        'networks': networks,
        'notification': notification,
    }
    return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'profile.html'), context)


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
            return redirect(f'/profile/{user.username}')
        else:
            messages.error(request, 'Такого пользователя не найдено')
    return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'login.html'), context)


def registration(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect(f'/profile/{request.user.username}')
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.is_active = False
            user = user_form.save()
            user.is_active = False
            user.save()
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
        else:
            if 'password2' in user_form.errors:
                invalid = user_form.errors['password2'][0]
                messages.error(request, invalid)
                context = {'form': user_form}
                return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'registration.html'),
                              context)
            else:
                messages.error(request, 'Что-то пошло не так, повторите попытку')
                context = {'form': user_form}
                return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'registration.html'),
                              context)
    user_form = CreateUserForm()
    context = {'form': user_form}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/account/', 'registration.html'), context)


def logout_def(request):
    logout(request)
    return redirect('/login')


def verification_email(request, user_id, token):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect(f'/profile/{request.user.username}')
    try:
        username = force_text(urlsafe_base64_decode(user_id))
        user = Account.objects.get(username=username)
        if token_generator.check_token(user, token) and not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Аккаунт успешко активирован')
            return redirect('/login')
        messages.error(request, 'Аккаунт по каким-то причинам не был активирован')
        return redirect('/login')
    except:
        pass
    return redirect('/login')
