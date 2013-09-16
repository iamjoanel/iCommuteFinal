from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from microposts.forms import MicropostForm
from microposts.models import Micropost

@login_required
def user_panel(request, title="User Home", template="accounts/profile.html", form = None):
    form = form or MicropostForm()
    posts = Micropost.objects.all().order_by('-created')[:10]
    return render_to_response(template, { 'form': form, 'next_url': '/accounts/profile', 'posts': posts}, RequestContext(request))
