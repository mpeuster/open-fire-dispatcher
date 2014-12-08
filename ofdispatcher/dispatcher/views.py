import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
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

    # helper to dynamically add content to choice fields
    def add_form_choices(form):
        # get loops that are valid for a contact and add them to form
        form.fields["loops"].choices = [
            (l.id, l.loop) for l in AlarmLoop.objects.filter(
                department=department)]

    if request.method == "POST":
        # POST request: process data
        # create form instance an add received data
        form = ContactForm(request.POST)
        add_form_choices(form)
        # check data and process it
        if form.is_valid():
            # create new contact
            c = form.save(commit=False)
            c.department = department
            c.save()
            # assign contact to loop(s)
            for loop_id in form.cleaned_data["loops"]:
                al = AlarmLoop.objects.get(id=int(loop_id))
                al.contacts.add(c)
            # redirect to new view
            return redirect("dispatcher:contacts")
    else:
        # GET request: return empty form
        form = ContactForm()
        add_form_choices(form)
    context = {"form": form}
    return render(request, "dispatcher/contact_create.html", context)


@login_required
def contact_update(request, id):
    c = Contact.objects.get(id=id)
    form = ContactForm(instance=c)
    context = {"contact": c, "form": form}
    return render(request, "dispatcher/contact_update.html", context)


@login_required
def contact_delete(request, id):
    pass
