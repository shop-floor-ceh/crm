from django.urls import path

from main import views

urlpatterns = [
    path('', views.main_page, name='home_page'),
    path('open_project', views.open_project, name='open_project'),
    path('create_project', views.create_project, name='create_project')
]
