from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.query import QuerySet

import os

from main.models import Project, Participant, Date
from main.forms import CreateProjectForm
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

    context = {
        'projects': projects,
    }
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
        if 'edit-project' in request.POST:
            project = Project.objects.get(pk=project_id)
            if 'name' in request.POST:
                project.name = request.POST['name']
            if 'about_project' in request.POST:
                project.about_project = request.POST['about_project']
            project.open_to_join = True if 'open_to_join' in request.POST else False
            project.ended = True if 'ended' in request.POST else False

            if 'synopsis' in request.FILES:
                project.synopsis = request.FILES['synopsis']
            if 'literary_script' in request.FILES:
                project.literary_script = request.FILES['literary_script']
            if 'directors_script' in request.FILES:
                project.directors_script = request.FILES['directors_script']
            if 'kpp' in request.FILES:
                project.kpp = request.FILES['kpp']
            try:
                project.save()
                messages.success(request, 'Успешно изменено')
                return redirect(f'/project/{project_id}')
            except:
                messages.error(request, 'Что-то пошло не так')
                return redirect(f'/project/{project_id}')
        if 'add-date' in request.POST:
            date = Date.objects.create(
                project=Project.objects.get(id=project_id),
                visiting_date=request.POST['visiting_date'],
                visiting_time=request.POST['visiting_time'],
                address=request.POST['address'],
                setting=request.POST['setting'],
                scene=request.POST['scene'],
                notify_send=False
            )
            date.save()
            messages.success(request, 'Дата успешно добавлена')
            return redirect(f'/project/{project_id}')
        if 'edit-date' in request.POST:
            date = Date.objects.get(id=request.POST['edit-date'])
            date.visiting_date = request.POST['visiting_date']
            date.visiting_time = request.POST['visiting_time']
            date.address = request.POST['address']
            date.setting = request.POST['setting']
            date.scene = request.POST['scene']
            date.notify_send = False
            date.save()
            return redirect(f'/project/{project_id}')
    try:
        project = Project.objects.get(pk=project_id)
        project.synopsis.name = '/'.join(project.synopsis.name.split('/')[1:])
        project.kpp.name = '/'.join(project.kpp.name.split('/')[1:])
        project.literary_script.name = '/'.join(project.literary_script.name.split('/')[1:])
        project.directors_script.name = '/'.join(project.directors_script.name.split('/')[1:])

        all_users = Account.objects.filter(is_active=True)

        user = request.user
        if project.admin == user:
            user.can_change_main_information = True
            user.can_add_participant = True
            user.can_change_synopsis = True
            user.can_change_literary_script = True
            user.can_change_directors_scripts = True
            user.can_change_kpp = True
            user.can_add_dates = True
        else:
            user.can_change_main_information = False
            user.can_add_participant = False
            user.can_change_synopsis = False
            user.can_change_literary_script = False
            user.can_change_directors_scripts = False
            user.can_change_kpp = False
            user.can_add_dates = False
        for participant in project.participants.all():
            if participant.participant == user:
                user.can_change_main_information = \
                    True if participant.can_change_main_information else user.can_change_main_information
                user.can_add_participant = \
                    True if participant.can_add_participant else user.can_add_participant
                user.can_change_synopsis = \
                    True if participant.can_change_synopsis else user.can_change_synopsis
                user.can_change_literary_script = \
                    True if participant.can_change_literary_script else user.can_change_literary_script
                user.can_change_directors_scripts = \
                    True if participant.can_change_directors_scripts else user.can_change_directors_scripts
                user.can_change_kpp = \
                    True if participant.can_change_kpp else user.can_change_kpp
                user.can_add_dates = \
                    True if participant.can_add_dates else user.can_add_dates

        dates = Date.objects.filter(project=project).order_by('visiting_date')

        context = {
            'project': project,
            'user': user,
            'all_users': all_users,
            'dates': dates
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
