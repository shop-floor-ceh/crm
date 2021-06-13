from django.shortcuts import render
from main.models import Project


def main_page(request):
    return render(request, 'home.html')


def open_project(request):
    project = Project.objects.filter(open_to_join=True)
    context = {'projects': project}
    return render(request, 'open_projects.html', context)
