import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from dispatcher.models import AlarmLoop, Contact
from dispatcher.forms import ContactForm


logger = logging.getLogger(__name__)


@login_required
def overview(request):
    return render(request, "dispatcher/overview.html", None)


@login_required
def alarms(request):
    return render(request, "dispatcher/alarms.html", None)


@login_required
def department(request):
    return render(request, "dispatcher/department.html", None)


@login_required
def loops(request):
    department = request.user.departmentmanager.department
    alarm_loop_list = AlarmLoop.objects.filter(department=department)
    context = {"alarm_loops": alarm_loop_list}
    return render(request, "dispatcher/loops.html", context)


@login_required
def contacts(request):
    department = request.user.departmentmanager.department
    contact_list = Contact.objects.filter(department=department)
    context = {"contacts": contact_list}
    return render(request, "dispatcher/contacts.html", context)


@login_required
def contact_create(request):
    if request.method == "POST":
        # POST request: process data
        # create form instance an add received data
        form = ContactForm(request.POST)
        # check data
        if form.is_valid():
            # TODO: process data
            # redirect to new view
            return HttpResponseRedirect(reverse("dispatcher:contacts"))
    else:
        # GET request: return empty form
        form = ContactForm()
    context = {"form": form}
    return render(request, "dispatcher/contact_create.html", context)


@login_required
def contact_update(request, id):
    context = {"action": str(id) + "/update"}
    return render(request, "dispatcher/contact_update.html", context)


@login_required
def contact_delete(request, id):
    pass
