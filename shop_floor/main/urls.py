from django.urls import path

from main import views

urlpatterns = [
    path('', views.main_page, name='home_page'),
    path('open_project', views.open_project, name='open_project'),
    path('create_project', views.create_project, name='create_project'),
    path('all_profiles', views.all_profiles, name='all_profiles'),
    path('calendar', views.calendar, name='calendar'),
    path('project/<project_id>', views.unique_project_page, name='project_page'),

]
