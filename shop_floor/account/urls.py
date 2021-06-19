from django.urls import path
from account import views

urlpatterns = [
    path('login', views.authorization, name='login_page'),
    path('registration', views.registration, name='registration_page'),
    path('logout', views.logout_def, name='logout_page'),
    # url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.profile_page, name='profile_page'),
    path('activate/<user_id>/<token>', views.verification_email, name='activate'),
    path('profile/<username>', views.profile_page, name='profile_page'),
    path('profile', views.all_profiles, name='all_profiles'),
]
