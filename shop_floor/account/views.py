from django.shortcuts import render


def authorization(request):
    return render(request, 'login.html')
