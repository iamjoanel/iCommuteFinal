from django.shortcuts import render_to_response
from django.template import RequestContext


def mobile(request, template="mobile/mobile-home.html"):
    return render_to_response(template, locals(), RequestContext(request)) 
