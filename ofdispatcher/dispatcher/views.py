import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
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
    # get department of user
    department = request.user.departmentmanager.department

    if request.method == "POST":
        # POST request: process data
        # create form instance an add received data
        form = ContactForm(request.POST)
        form.update_loop_choices(department)
        # check data and process it
        if form.is_valid():
            # create new contact
            c = form.save(commit=False)
            c.department = department
            c.save()
            c.update_alarmloop_assignment(form.cleaned_data["loops"])
            # redirect to list view
            return redirect("dispatcher:contacts")
    else:
        # GET request: return empty form
        form = ContactForm()
        form.update_loop_choices(department)
    context = {"form": form}
    return render(request, "dispatcher/contact_create.html", context)


@login_required
def contact_update(request, id):
    # get department of user
    department = request.user.departmentmanager.department
    # get Contact from model that should be updated
    c = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        # POST request: process data
        # create form instance an add received data
        form = ContactForm(request.POST, instance=c)
        form.update_loop_choices(department)
        # check data and process it
        if form.is_valid():
            form.save()
            c.update_alarmloop_assignment(form.cleaned_data["loops"])
            # redirect to list view
            return redirect("dispatcher:contacts")
    else:
        # GET request: return initial form
        form = ContactForm(instance=c)
        form.update_loop_choices(department, c)
    context = {"contact": c, "form": form}
    return render(request, "dispatcher/contact_update.html", context)


@login_required
def contact_delete(request, id):
    pass
