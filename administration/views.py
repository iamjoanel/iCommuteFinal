from django.contrib.auth import authenticate, login, logout
from django.shortcuts import (redirect, render_to_response)
from django.contrib import messages
from django.template import RequestContext



def administration_login(request, template="administration/login.html"):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_superuser:
            login(request, user)
            return redirect('route_home')
        else:
            messages.add_message(request, messages.ERROR, "Not an Administrator Account")

    return render_to_response(template, locals(), RequestContext(request))


def administration_logout(request):
    logout(request)
    return redirect('administration_login')
