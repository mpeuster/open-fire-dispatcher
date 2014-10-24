from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def overview(request):
    return render(request, 'dispatcher/overview.html', None)


@login_required
def alarms(request):
    return render(request, 'dispatcher/alarms.html', None)


@login_required
def department(request):
    return render(request, 'dispatcher/department.html', None)


@login_required
def loops(request):
    return render(request, 'dispatcher/loops.html', None)


@login_required
def contacts(request):
    return render(request, 'dispatcher/contacts.html', None)
