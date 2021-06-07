from django.urls import path

from account import views

urlpatterns = [
    path('login', views.authorization, name='login_page'),
    path('registration', views.registration, name='registration_page'),
    path('profile', views.profile_page, name='profile_page'),
    path('logout', views.logout_def, name='logout_page'),
]
