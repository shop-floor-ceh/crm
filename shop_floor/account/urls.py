from django.urls import path

from account import views

urlpatterns = [
    path('login', views.authorization, name='login_page'),
    path('registration', views.registration, name='registration_page'),
]
