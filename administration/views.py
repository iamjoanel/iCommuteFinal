from django.contrib.auth import authenticate, login, logout
from django.shortcuts import (redirect, render_to_response)
from django.contrib import messages
from django.template import RequestContext

from .forms import LoginForm

def administration_login(request, template="administration/login.html"):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('route_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = LoginForm()

    return render_to_response(template, locals(), RequestContext(request))

def administration_logout(request):
    logout(request)
    return redirect('administration_login')
