import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dispatcher.models import AlarmLoop


logger = logging.getLogger(__name__)


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
    department = request.user.departmentmanager.department
    alarm_loop_list = AlarmLoop.objects.filter(department=department)
    context = {"alarm_loops": alarm_loop_list}
    return render(request, 'dispatcher/loops.html', context)


@login_required
def contacts(request):
    return render(request, 'dispatcher/contacts.html', None)
