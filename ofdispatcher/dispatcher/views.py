from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def overview(request):
    return render(request, 'dispatcher/overview.html', None)
