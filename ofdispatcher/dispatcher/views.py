from django.shortcuts import render


def home(request):
    return render(request, 'dispatcher/home.html', None)
