from django.shortcuts import render, redirect
from django.contrib import messages

import os

from main.models import Project, Participant
from main.forms import CreateProjectForm
from account.models import Account
from shop_floor.settings import BASE_DIR


def main_page(request):
    user = Account.objects.get(username=request.user.username)
    participants = Participant.objects.filter(participant=user)
    projects = set()
    for i in participants:
        x = Project.objects.get(participants=i)
        if x:
            projects.add(x)
    context = {'projects': projects}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'home.html'), context)


def open_project(request):
    project = Project.objects.filter(open_to_join=True)
    context = {'projects': project}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'open_projects.html'), context)


def create_project(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    form = CreateProjectForm()
    users = Account.objects.all()
    context = {'form': form, 'users': users}
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            print(request.POST)
            instance = form.save()
            print(instance.synopsis)
            return redirect('/profile')
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'create_project.html'), context)
