import json
from django.shortcuts import (render_to_response, redirect, get_object_or_404)
from django.template import RequestContext
from django.contrib import messages
from django.views.generic import DeleteView, TemplateView
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from vectorformats.Formats import Django, GeoJSON
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse

from .forms import (TrainPathForm, PathForm, RouteForm)
from .models import (TrainPath, Path, Route)
from .utils import (calculate_cost, calculate_train_cost, distance_total, cost_total)
from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback

def route_home(request, template="route/route/home.html", title="Route Management"):
    if request.user.is_superuser:
        route_list = Route.objects.all().order_by('-created')
        route_paginator = Paginator(route_list, 10)
        page = request.GET.get('page')

        try:
            route = route_paginator.page(page)
        except PageNotAnInteger:
            route = route_paginator.page(1)
        except EmptyPage:
            route = route_paginator.page(route_paginator.num_pages)

        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')


def add_route(request, template="route/route/route-form.html", title="Add Route"):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = RouteForm(request.POST)
            form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
            form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
            if form.is_valid():
                instance = form.save(commit=False)
                origin = instance.origin.strip(' \t\n\r').split(',')
                destination = instance.destination.strip(' \t\n\r').split(',')

                try:
                    x = origin[1]
                    y = destination[1]
                except IndexError:
                    messages.add_message(request, messages.ERROR, "No Origin City or Destination City")
                    form = RouteForm(request.POST, instance=instance)
                    return render_to_response(template, locals(), RequestContext(request))

                if x and y:
                    instance.origin = origin[0]
                    instance.origin_city = origin[1].lstrip()
                    instance.destination = destination[0]
                    instance.destination_city = destination[1].lstrip()

                instance.created_by = request.user
                instance.save()
                form.save_m2m()
                instance.total_distance = distance_total(instance)
                instance.total_cost = cost_total(instance)

                instance.save()

                messages.add_message(request, messages.SUCCESS, 'Route added successfully!')
                return redirect('route_home')
            else:
                messages.add_message(request, messages.ERROR, ''.join(
                    form.non_field_errors()))
        else:
            form = RouteForm()
            form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
            form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')


class DeleteRouteView(DeleteView):
    model = Route
    template_name = 'route/route/delete-route.html'

    def get_success_url(self):
        return reverse('route_home')


def edit_route(request, pk, template="route/route/route-form.html", title="Edit Route"):
    if request.user.is_superuser:
        route_object = get_object_or_404(Route, pk=pk)
        if request.method == 'POST':
            form = RouteForm(request.POST, instance=route_object)
            form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
            form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
            if form.is_valid():
                instance = form.save(commit=False)
                origin = instance.origin.split(',')
                destination = instance.destination.split(',')

                try:
                    x = origin[1]
                    y = destination[1]
                except IndexError:
                    messages.add_message(request, messages.ERROR, "No Origin City or Destination City")
                    form = RouteForm(request.POST, instance=instance)
                    return render_to_response(template, locals(), RequestContext(request))

                if x and y:
                    instance.origin = origin[0]
                    instance.origin_city = origin[1].lstrip()
                    instance.destination = destination[0]
                    instance.destination_city = destination[1].lstrip()

                instance.save()
                form.save_m2m()
                instance.total_distance = distance_total(instance)
                instance.total_cost = cost_total(instance)
                instance.save()

                messages.add_message(request, messages.SUCCESS, 'Route added successfully!')
                return redirect('route_home')
            else:
                messages.add_message(request, messages.ERROR, ''.join(
                    form.non_field_errors()))
        else:
            form = RouteForm(instance=route_object)
            form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
            form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')


def review_route(request, pk, template="route/route/view-route.html", title="Review Route"):
    if request.user.is_superuser:
        route = get_object_or_404(Route, pk=pk)
        path = route.path.all()
        train_path = route.train_path.all()
        geoj = GeoJSON.GeoJSON()

        path_format = Django.Django(geodjango="path", properties=["mode"])
        path_json = geoj.encode(path_format.decode(path))
        train_path_format = Django.Django(geodjango="path")
        train_path_json = geoj.encode(train_path_format.decode(train_path))

        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')

def approve_route(request, pk):
    if request.user.is_superuser:
        route = get_object_or_404(Route, pk=pk)
        if request.user.is_superuser:
            if not route.is_approved:
                route.is_approved = True
                route.save()
                messages.add_message(request, messages.SUCCESS, 'Route Approved')
                op = True
                notify_approval(route.pk, op)
            else:
                route.is_approved = False
                op = False
                route.save()
                messages.add_message(request, messages.ERROR, 'Route Disapproved')
                notify_approval(route.pk, op)
            return redirect('route_home')
    else:
        return redirect('user_panel')

def notify_approval(pk, op):
    route = get_object_or_404(Route, pk=pk)
    user = get_object_or_404(User, pk=route.created_by.pk)
    receiver = user.email
    if op:
        subject = "Route Approved"

        message = "This is to notify you that the Route: %s you created on: %s was approved by the administrator\n\n\n\n\n iCommute Administrator" % (route, route.created)
    else:
        subject = "Route Disapproved"
        message = "This is to notify you that the Route: %s you created on: %s was disapproved by the administrator\n\n\n\n\n iCommute Administrator" % (route, route.created)

    send_mail(subject, message, "admin@icommute-ph.com", [receiver], fail_silently=False)

 # Path Views
def path_home(request, template="route/path/home.html", title="Path Management"):
    if request.user.is_superuser:
        path_list = Path.objects.all().order_by('-created')
        path_paginator = Paginator(path_list, 10)
        page = request.GET.get('page')

        try:
            path = path_paginator.page(page)
        except PageNotAnInteger:
            path = path_paginator.page(1)
        except EmptyPage:
            path = path_paginator.page(path_paginator.num_pages)

        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')

def add_path(request, template="route/path/path-form.html", title="Add Path"):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = PathForm(request.POST)
            distance = 0
            if form.is_valid():
                path_object = form.save()
                path_object.save()
                for p in Path.objects.filter(pk=path_object.pk).length():
                    if path_object.mode == 'Walk':
                        if p.length.km > 0.3:
                            messages.add_message(request, messages.ERROR, 'Maximum walking distance is 300m')
                            form = PathForm(instance=path_object)
                            return render_to_response(template, locals(), RequestContext(request))
                        else:
                            distance = p.length.km
                            path_object.cost = 0
                    else:
                        distance = p.length.km
                        path_object.cost = calculate_cost(path_object.mode, distance)

                    path_object.distance = distance
                    path_object.created_by = request.user
                    path_object.save()
                    messages.add_message(request, messages.SUCCESS, "Path Added Successfully")
                    return redirect('path_home')

            else:
                messages.add_message(request, messages.ERROR, ''.join(
                    form.non_field_errors()))
        else:
            form = PathForm()
        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')


class DeletePathView(DeleteView):
    model = Path
    template_name = 'route/path/delete-path.html'

    def get_success_url(self):
        return reverse('path_home')


def edit_path(request, pk, template="route/path/path-form.html", title="Edit Path"):
    if request.user.is_superuser:
        path_object = get_object_or_404(Path, pk=pk)
        if request.method == 'POST':
            form = PathForm(request.POST, instance=path_object)
            if form.is_valid():
                path_object = form.save()
                path_object.save()
                for p in Path.objects.filter(pk=path_object.pk).length():
                    if path_object.mode == 'Walk':
                        if p.length.km > 0.3:
                            messages.add_message(request, messages.ERROR, 'Maximum walking distance is 300m')
                            form = PathForm(instance=path_object)
                            return render_to_response(template, locals(), RequestContext(request))
                        else:
                            distance = p.length.km
                            path_object.cost = 0

                    else:
                        distance = p.length.km
                        path_object.cost = calculate_cost(path_object.mode, distance)

                    path_object.distance = distance
                    path_object.save()
                    messages.add_message(request, messages.SUCCESS, "Path Updated Successfully")
                    return redirect('path_home')
            else:
                messages.add_message(request, messages.ERROR, ''.join(
                    form.non_field_errors()))
        else:
            form = PathForm(instance=path_object)
        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')
# End of Path view

# Train Path views
def train_path_home(request, template="route/train path/home.html", title="Train Path Management"):
    if request.user.is_superuser:
        train_path_list = TrainPath.objects.all().order_by('-created')
        train_path_paginator = Paginator(train_path_list, 10)
        page = request.GET.get('page')

        try:
            train_path = train_path_paginator.page(page)
        except PageNotAnInteger:
            train_path = train_path_paginator.page(1)
        except EmptyPage:
            train_path = train_path_paginator.page(train_path_paginator.num_pages)

        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')


def add_train_path(request, template="route/train path/train-path-form.html", title="Add Train Path"):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = TrainPathForm(request.POST)
            if form.is_valid():
                instance = form.save()
                instance.cost = calculate_train_cost(instance.origin_station, instance.destination_station)
                for p in TrainPath.objects.filter(pk=instance.pk).length():
                    instance.distance = p.length.km
                instance.created_by = request.user
                instance.save()
                messages.add_message(request, messages.SUCCESS, "Train Path added successfully")
                return redirect('train_path_home')
            else:
                messages.add_message(request, messages.ERROR, ''.join(form.non_field_errors()))
        else:
            form = TrainPathForm()
            return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')


class DeleteTrainPathView(DeleteView):
    model = TrainPath
    template_name = 'route/train path/delete-train-path.html'

    def get_success_url(self):
        return reverse('train_path_home')


def edit_train_path(request, pk, template="route/train path/train-path-form.html", title="Edit Train Path"):
    if request.user.is_superuser:
        train_path_object = get_object_or_404(TrainPath, pk=pk)
        if request.method == 'POST':
            form = TrainPathForm(request.POST, instance=train_path_object)
            if form.is_valid():
                instance = form.save()
                instance.cost = calculate_train_cost(instance.origin_station, instance.destination_station)
                for p in TrainPath.objects.filter(pk=instance.pk).length():
                    instance.distance = p.length.km
                instance.save()
                messages.add_message(request, messages.SUCCESS, "Train Path added successfully")
                return redirect('train_path_home')
            else:
                messages.add_message(request, messages.ERROR, ''.join(form.non_field_errors()))
        else:
            form = TrainPathForm(instance=train_path_object)
        return render_to_response(template, locals(), RequestContext(request))
    else:
        return redirect('user_panel')

"""
Public Route Views
"""
@login_required
def public_add_route(request, template="route/public/route/route-form.html", title="Add Route"):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
        form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            origin = instance.origin.split(',')
            destination = instance.destination.split(',')

            try:
                x = origin[1]
                y = destination[1]
            except IndexError:
                messages.add_message(request, messages.ERROR, "No Origin City or Destination City")
                form = RouteForm(request.POST, instance=instance)
                return render_to_response(template, locals(), RequestContext(request))

            if x and y:
                instance.origin = origin[0]
                instance.origin_city = origin[1].lstrip()
                instance.destination = destination[0]
                instance.destination_city = destination[1].lstrip()

            instance.created_by = request.user
            instance.save()
            form.save_m2m()
            instance.total_distance = distance_total(instance)
            instance.total_cost = cost_total(instance)

            instance.save()

            messages.add_message(request, messages.SUCCESS, 'Route added successfully!')
            return redirect('public_route_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = RouteForm()
        form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
        form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
    return render_to_response(template, locals(), RequestContext(request))


class PublicDeleteRouteView(DeleteView):
    model = Route
    template_name = 'route/public/route/delete-route.html'

    def get_success_url(self):
        return reverse('public_route_home')


@login_required
def public_edit_route(request, pk, template="route/public/route/route-form.html", title="Edit Route"):
    route_object = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route_object)
        form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
        form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            origin = instance.origin.split(',')
            destination = instance.destination.split(',')
            instance.is_approved = False

            try:
                x = origin[1]
                y = destination[1]
            except IndexError:
                messages.add_message(request, messages.ERROR, "No Origin City or Destination City")
                form = RouteForm(request.POST, instance=instance)
                return render_to_response(template, locals(), RequestContext(request))

            if x and y:
                instance.origin = origin[0]
                instance.origin_city = origin[1].lstrip()
                instance.destination = destination[0]
                instance.destination_city = destination[1].lstrip()

            instance.save()
            form.save_m2m()
            instance.total_distance = distance_total(instance)
            instance.total_cost = cost_total(instance)
            instance.save()

            messages.add_message(request, messages.SUCCESS, 'Route added successfully!')
            return redirect('public_route_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = RouteForm(instance=route_object)
        form.fields["path"].queryset = Path.objects.filter(created_by=request.user)
        form.fields["train_path"].queryset = TrainPath.objects.filter(created_by=request.user)
    return render_to_response(template, locals(), RequestContext(request))

@login_required
def public_add_path(request, template="route/public/path/path-form.html", title="Add Path"):
    if request.method == 'POST':
        form = PathForm(request.POST)
        distance = 0
        if form.is_valid():
            path_object = form.save()
            path_object.save()
            for p in Path.objects.filter(pk=path_object.pk).length():
                if path_object.mode == 'Walk':
                    if p.length.km > 0.3:
                        messages.add_message(request, messages.ERROR, 'Maximum walking distance is 300m')
                        form = PathForm(instance=path_object)
                        return render_to_response(template, locals(), RequestContext(request))
                    else:
                        distance = p.length.km
                        path_object.cost = 0
                else:
                    distance = p.length.km
                    path_object.cost = calculate_cost(path_object.mode, distance)

                path_object.distance = distance
                path_object.created_by = request.user
                path_object.save()
                messages.add_message(request, messages.SUCCESS, "Path Added Successfully")
                return redirect('public_path_home')

        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = PathForm()
    return render_to_response(template, locals(), RequestContext(request))


class PublicDeletePathView(DeleteView):
    model = Path
    template_name = 'route/public/path/delete-path.html'

    def get_success_url(self):
        return reverse('public_path_home')

@login_required
def public_edit_path(request, pk, template="route/public/path/path-form.html", title="Edit Path"):
    path_object = get_object_or_404(Path, pk=pk)
    if request.method == 'POST':
        form = PathForm(request.POST, instance=path_object)
        if form.is_valid():
            path_object = form.save()
            path_object.save()
            for p in Path.objects.filter(pk=path_object.pk).length():
                if path_object.mode == 'Walk':
                    if p.length.km > 0.3:
                        messages.add_message(request, messages.ERROR, 'Maximum walking distance is 300m')
                        form = PathForm(instance=path_object)
                        return render_to_response(template, locals(), RequestContext(request))
                    else:
                        distance = p.length.km
                        path_object.cost = 0

                else:
                    distance = p.length.km
                    path_object.cost = calculate_cost(path_object.mode, distance)

                path_object.distance = distance
                path_object.save()
                messages.add_message(request, messages.SUCCESS, "Path Updated Successfully")
                return redirect('public_path_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = PathForm(instance=path_object)
    return render_to_response(template, locals(), RequestContext(request))
# End of Path view

@login_required
def public_add_train_path(request, template="route/public/train path/train-path-form.html", title="Add Train Path"):
    if request.method == 'POST':
        form = TrainPathForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.cost = calculate_train_cost(instance.origin_station, instance.destination_station)
            for p in TrainPath.objects.filter(pk=instance.pk).length():
                instance.distance = p.length.km
            instance.created_by = request.user
            instance.save()
            messages.add_message(request, messages.SUCCESS, "Train Path added successfully")
            return redirect('public_train_path_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(form.non_field_errors()))
    else:
        form = TrainPathForm()
        return render_to_response(template, locals(), RequestContext(request))


class PublicDeleteTrainPathView(DeleteView):
    model = TrainPath
    template_name = 'route/public/train path/delete-train-path.html'

    def get_success_url(self):
        return reverse('public_train_path_home')

@login_required
def public_edit_train_path(request, pk, template="route/public/train path/train-path-form.html", title="Edit Train Path"):
    train_path_object = get_object_or_404(TrainPath, pk=pk)
    if request.method == 'POST':
        form = TrainPathForm(request.POST, instance=train_path_object)
        if form.is_valid():
            instance = form.save()
            instance.cost = calculate_train_cost(instance.origin_station, instance.destination_station)
            for p in TrainPath.objects.filter(pk=instance.pk).length():
                instance.distance = p.length.km
            instance.save()
            messages.add_message(request, messages.SUCCESS, "Train Path added successfully")
            return redirect('public_train_path_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(form.non_field_errors()))
    else:
        form = TrainPathForm(instance=train_path_object)
    return render_to_response(template, locals(), RequestContext(request))

@login_required
def public_route_home(request, template="route/public/route/home.html", title="Route Management"):
    route_list = Route.objects.filter(created_by=request.user).order_by('-created')
    route_paginator = Paginator(route_list, 10)
    page = request.GET.get('page')

    try:
        route = route_paginator.page(page)
    except PageNotAnInteger:
        route = route_paginator.page(1)
    except EmptyPage:
        route = route_paginator.page(route_paginator.num_pages)

    return render_to_response(template, locals(), RequestContext(request))

@login_required
def public_path_home(request, template="route/public/path/home.html", title="Path Management"):
        path_list = Path.objects.filter(created_by=request.user).order_by('-created')
        path_paginator = Paginator(path_list, 10)
        page = request.GET.get('page')

        try:
            path = path_paginator.page(page)
        except PageNotAnInteger:
            path = path_paginator.page(1)
        except EmptyPage:
            path = path_paginator.page(path_paginator.num_pages)

        return render_to_response(template, locals(), RequestContext(request))

@login_required
def public_train_path_home(request, template="route/public/train path/home.html", title="Train Path Management"):
    train_path_list = TrainPath.objects.filter(created_by=request.user).order_by('-created')
    train_path_paginator = Paginator(train_path_list, 10)
    page = request.GET.get('page')

    try:
        train_path = train_path_paginator.page(page)
    except PageNotAnInteger:
        train_path = train_path_paginator.page(1)
    except EmptyPage:
        train_path = train_path_paginator.page(train_path_paginator.num_pages)

    return render_to_response(template, locals(), RequestContext(request))


@login_required
def view_route(request, pk, template="route/public/route/view-route.html"):
    route = get_object_or_404(Route, pk=pk)
    if route.is_approved == False:
        return redirect('view_route_error')
    else:
        path = route.path.all()
        train_path = route.train_path.all()
        geoj = GeoJSON.GeoJSON()
        form = FeedbackForm()
        feedbacks = Feedback.objects.filter(route=route.pk).filter(approved=True).order_by('-date_posted')

        path_format = Django.Django(geodjango="path", properties=["mode"])
        path_json = geoj.encode(path_format.decode(path))
        train_path_format = Django.Django(geodjango="path")
        train_path_json = geoj.encode(train_path_format.decode(train_path))

        return render_to_response(template, locals(), RequestContext(request))

@login_required
def search_route(request, template="route/public/route/results.html"):
    if 'origin' and 'destination' in request.GET:
        origin = request.GET['origin']
        destination = request.GET['destination']

        if origin and destination is not None:
            query = origin + " To " + destination
            routes_found = Route.objects.filter(is_approved=True).filter(origin__iexact=origin).filter(destination__iexact=destination).order_by('total_distance', 'total_cost')

    return render_to_response(template, locals(), RequestContext(request))

class ViewError(TemplateView):
    template_name = "route/public/route/error.html"


def get_origin(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        routes = Route.objects.filter(origin__icontains = q).filter(is_approved=True)[:20]
        results = []
        for route in routes:
            route_json = {}
            route_json['id'] = route.pk
            route_json['label'] = route.origin
            route_json['id'] = route.origin
            results.append(route_json)
        data = json.dumps(results)
    else:
        data = 'Fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def get_destination(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        routes = Route.objects.filter(destination__icontains = q).filter(is_approved=True)[:20]
        results = []
        for route in routes:
            route_json = {}
            route_json['id'] = route.pk
            route_json['label'] = route.destination
            route_json['id'] = route.destination
            results.append(route_json)
        data = json.dumps(results)
    else:
        data = 'Fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)
