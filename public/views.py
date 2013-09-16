from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request, template="public/home.html"):
    return render_to_response(template, locals(), RequestContext(request))

def mobile(request, template="public/mobile-home.html"):
    return render_to_response(template, locals(), RequestContext(request))  
