from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def user_panel(request, title="User Home", template="accounts/profile.html"):
    return render_to_response(template, locals(), RequestContext(request))
