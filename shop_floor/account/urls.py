from django.urls import path
from django.conf.urls import url
from account import views

urlpatterns = [
    path('login', views.authorization, name='login_page'),
    path('registration', views.registration, name='registration_page'),
    path('logout', views.logout_def, name='logout_page'),
    # url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.profile_page, name='profile_page'),
    path('profile', views.profile_page, name='profile_page'),
]
