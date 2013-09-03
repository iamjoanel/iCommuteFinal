from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from report.forms import ReportForm

@login_required
def user_panel(request, title="User Home", template="accounts/profile.html"):
    report_form = ReportForm()
    return render_to_response(template, locals(), RequestContext(request))
