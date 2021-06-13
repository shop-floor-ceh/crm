from django.shortcuts import render
from main.models import Project, Participant
from account.models import Account
from shop_floor.settings import BASE_DIR
import os


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
