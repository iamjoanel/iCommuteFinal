from django.template import RequestContext
from django.shortcuts import (render_to_response, redirect)


def home(request, template="public/home.html"):
    return render_to_response(template, locals(), RequestContext(request))
