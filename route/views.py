from django.shortcuts import (render_to_response, redirect, get_object_or_404)
from django.template import RequestContext
from django.contrib import messages
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import (TrainPathForm, PathForm, RouteForm)
from .models import (TrainPath, Path, Route)
from .utils import (calculate_cost, calculate_train_cost)


def route_home(request, template="route/route/home.html", title="Route Management"):

    route_list = Route.objects.all()
    route_paginator = Paginator(route_list, 10)
    page = request.GET.get('page')

    try:
        route = route_paginator.page(page)
    except PageNotAnInteger:
        route = route_paginator.page(1)
    except EmptyPage:
        route = route_paginator.page(route_paginator.num_pages)

    return render_to_response(template, locals(), RequestContext(request))

# Path Views
def path_home(request, template="route/path/home.html", title="Route Management"):

    path_list = Path.objects.all()
    path_paginator = Paginator(path_list, 10)
    page = request.GET.get('page')

    try:
        path = path_paginator.page(page)
    except PageNotAnInteger:
        path = path_paginator.page(1)
    except EmptyPage:
        path = path_paginator.page(path_paginator.num_pages)

    return render_to_response(template, locals(), RequestContext(request))


def add_path(request, template="route/path/path-form.html", title="Add Path"):
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
                path_object.save()
                messages.add_message(request, messages.SUCCESS, "Path Added Successfully")
                return redirect('path_home')

        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = PathForm()
    return render_to_response(template, locals(), RequestContext(request))


class DeletePathView(DeleteView):
    model = Path
    template_name = 'route/path/delete-path.html'

    def get_success_url(self):
        return reverse('path_home')


def edit_path(request, pk, template="route/path/path-form.html", title="Add Path"):
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
# End of Path view

# Train Path views
def train_path_home(request, template="route/train path/home.html", title="Route Management"):

    train_path_list = TrainPath.objects.all()
    train_path_paginator = Paginator(train_path_list, 10)
    page = request.GET.get('page')

    try:
        train_path = train_path_paginator.page(page)
    except PageNotAnInteger:
        train_path = train_path_paginator.page(1)
    except EmptyPage:
        train_path = train_path_paginator.page(train_path_paginator.num_pages)

    return render_to_response(template, locals(), RequestContext(request))


def add_train_path(request, template="route/train path/train-path-form.html", title="Add Train Path"):
    if request.method == 'POST':
        form = TrainPathForm(request.POST)
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
        form = TrainPathForm()
        return render_to_response(template, locals(), RequestContext(request))


class DeleteTrainPathView(DeleteView):
    model = TrainPath
    template_name = 'route/train path/delete-train-path.html'

    def get_success_url(self):
        return reverse('train_path_home')


def edit_train_path(request, pk, template="route/train path/train-path-form.html", title="Edit Train Path"):
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
