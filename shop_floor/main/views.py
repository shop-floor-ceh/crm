from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.query import QuerySet

import os

from main.models import Project, Participant
from main.forms import CreateProjectForm, CreateParticipantForm
from account.models import Account
from shop_floor.settings import BASE_DIR


def main_page(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    user = Account.objects.get(username=request.user.username)
    participants = Participant.objects.filter(participant=user)
    projects = set()
    for i in participants:
        x = Project.objects.filter(participants=i)

        if x:
            if type(x) is QuerySet:
                for j in list(x):
                    projects.add(j)
            else:
                projects.add(x)
    context = {'projects': projects}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'home.html'), context)


def unique_project_page(request, project_id):
    if request.method == 'POST':
        if 'add-participants' in request.POST:
            project = Project.objects.get(pk=project_id)
            participant = Participant.objects.create(
                participant=Account.objects.get(id=request.POST['participant']),
                name=request.POST['name'],
                can_change_main_information=True if 'can_change_main_information' in request.POST else False,
                can_add_participant=True if 'can_add_participant' in request.POST else False,
                can_change_synopsis=True if 'can_change_synopsis' in request.POST else False,
                can_change_literary_script=True if 'can_change_literary_script' in request.POST else False,
                can_change_directors_scripts=True if 'can_change_directors_scripts' in request.POST else False,
                can_change_kpp=True if 'can_change_kpp' in request.POST else False,
                can_add_dates=True if 'can_add_dates' in request.POST else False,

            )
            project.participants.add(participant)
            return redirect(f'/project/{project_id}')
    try:
        form = CreateParticipantForm()
        project = Project.objects.get(pk=project_id)
        project.synopsis.name = '/'.join(project.synopsis.name.split('/')[1:])
        project.kpp.name = '/'.join(project.kpp.name.split('/')[1:])
        project.literary_script.name = '/'.join(project.literary_script.name.split('/')[1:])
        project.directors_script.name = '/'.join(project.directors_script.name.split('/')[1:])
        context = {
            'project': project,
            'form': form
        }
        return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'project.html'), context)
    except:
        messages.error(request, 'Такого проекта нет')
        return redirect('/open_project')


def open_project(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
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
            instance = form.save()
            participant = Participant(
                participant=request.user,
                name='Aдмин',
                can_add_participant=True,
                can_change_synopsis=True,
                can_change_literary_script=True,
                can_change_directors_scripts=True,
                can_change_kpp=True,
                can_add_dates=True
            )
            participant.save()
            instance.participants.add(participant)
            return redirect(f'/project/{instance.id}')
        else:
            messages.error(request, 'Что-то пошло не так попробуй еще раз')
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'create_project.html'), context)


def calendar(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    context = {}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'calendar.html'), context)
