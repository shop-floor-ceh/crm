from django.shortcuts import render
from main.models import Project
from shop_floor.settings import BASE_DIR
import os


def main_page(request):
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'home.html'))


def open_project(request):
    project = Project.objects.filter(open_to_join=True)
    context = {'projects': project}
    return render(request, os.path.join(str(BASE_DIR) + '/templates/main/', 'open_projects.html'), context)
