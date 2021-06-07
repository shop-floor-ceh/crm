from django.shortcuts import render


def authorization(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')
