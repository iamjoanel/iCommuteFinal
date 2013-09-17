from django.shortcuts import (render_to_response, redirect)
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from microposts.forms import MicropostForm
from microposts.models import Micropost


def home(request, template="mobile/mobile-home.html"):
    form = MicropostForm()
    posts = Micropost.objects.all().order_by('-created')[:10]
    return render_to_response(template, locals(), RequestContext(request))

@login_required
def m_user(request, template="mobile/user-panel.html"):
    form = MicropostForm()
    posts = Micropost.objects.all().order_by('-created')[:10]
    return render_to_response(template, locals(), RequestContext(request))

@login_required
def m_login(request, template="mobile/mobile-login.html"):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_authenticated:
                    login(request, user)
                    return redirect('mobile_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = LoginForm()

    return render_to_response(template, locals(), RequestContext(request))

    
@login_required
def m_logout(request):
    logout(request)
    return redirect('m_login')
