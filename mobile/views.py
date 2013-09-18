import json
from django.http import HttpResponse
from django.shortcuts import (render_to_response, redirect, get_object_or_404)
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from vectorformats.Formats import Django, GeoJSON
from django.views.generic import TemplateView

from .forms import LoginForm
from microposts.forms import MobileForm
from microposts.models import Micropost
from route.models import Route
from feedbacks.forms import FeedbackFormMobile
from feedbacks.models import Feedback
from requests.forms import MobileRequestForm
from requests.models import Request


@login_required
def home(request, template="mobile/mobile-home.html"):
    form = MobileForm()
    posts = Micropost.objects.all().order_by('-created')[:10]
    return render_to_response(template, locals(), RequestContext(request))


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


def m_logout(request):
    logout(request)
    return redirect('m_login')


@login_required
def m_new_report(request):
    if request.method == 'POST':
        form = MobileForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('mobile_home')
        else:
            return home(request, form)
    return redirect('/')


@login_required
def m_view_route(request, pk, template="mobile/view-route.html"):
    route = get_object_or_404(Route, pk=pk)
    if route.is_approved == False:
        return redirect('mobile_route_error')
    else:
        path = route.path.all()
        train_path = route.train_path.all()
        geoj = GeoJSON.GeoJSON()
        form = FeedbackFormMobile()
        feedbacks = Feedback.objects.filter(route=route.pk).filter(approved=True).order_by('-date_posted')

        path_format = Django.Django(geodjango="path", properties=["mode"])
        path_json = geoj.encode(path_format.decode(path))
        train_path_format = Django.Django(geodjango="path")
        train_path_json = geoj.encode(train_path_format.decode(train_path))

        return render_to_response(template, locals(), RequestContext(request))

@login_required
def m_search_route(request, template="mobile/search-route.html"):
    if 'origin' and 'destination' in request.GET:
        origin = request.GET['origin']
        destination = request.GET['destination']

        if origin and destination is not None:
            query = origin + " To " + destination
            routes_found = Route.objects.filter(is_approved=True).filter(origin__iexact=origin).filter(destination__iexact=destination).order_by('total_distance', 'total_cost')
            template = "mobile/results.html"

    return render_to_response(template, locals(), RequestContext(request))

class MobileViewError(TemplateView):
    template_name = "mobile/error.html"

@login_required
def m_new_requests(request, template="mobile/request-form.html"):
    if request.method == 'POST':
        form = MobileRequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)

            try:
                request_object = Request.objects.get(origin__iexact=request_instance.origin, destination__iexact=request_instance.destination)
            except Request.DoesNotExist:
                request_object = None

            if request_object is None:
                request_instance.requested_by = request.user
                request_instance.count = 1
                request_instance.save()
                messages.add_message(request, messages.SUCCESS, 'Route requested')
            else:
                request_object.requested_by = request.user
                request_object.count += 1
                request_object.save()
                messages.add_message(request, messages.SUCCESS, 'Route requested')
        else:
            messages.add_message(request, messages.ERROR,
                                 'You need to fill in  the required fields!')
        return redirect('m_new_requests')
    else:
        form = MobileRequestForm()
    return render_to_response(template, locals(), RequestContext(request))


def m_add_feedback(request):
    if request.method == 'POST':
        message = "Somethings Wrong with your feedback"
        form = FeedbackFormMobile(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            message = 'Your comment has been sent and is under administrator inspection'

    return HttpResponse(json.dumps({'message': message}))
