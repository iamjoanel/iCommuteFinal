from django.shortcuts import (render_to_response, redirect, get_object_or_404)
from django.template import RequestContext
from django.contrib import messages
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import (TrainPathForm, PathForm, RouteForm)
from .models import (TrainPath, Path, Route)


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


def add_path(request, template="route/path/path-form.html", title="Add Path"):
    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            path_object = form.save()
            path_object.save()
            for p in Path.objects.filter(pk=path_object.pk).length():
                if path_object.mode == 'Walk':
                    path_object.cost = 0
                    if p.length > 0.3:
                        messages.add_message(request, messages.ERROR, 'Maximum walking distance is 300m')
                    else:
                        distance = p.length.km
                else:
                    distance = p.length.km
                    path_object.cost = 1

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
                    path_object.cost = 0
                    if p.length > 0.3:
                        messages.add_message(request, messages.ERROR, 'Maximum walking distance is 300m')
                    else:
                        distance = p.length.km
                else:
                    distance = p.length.km
                    path_object.cost = 1

                path_object.distance = distance
                path_object.save()
                messages.add_message(request, messages.SUCCESS, "Path Added Successfully")
                return redirect('path_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(
                form.non_field_errors()))
    else:
        form = PathForm(instance=path_object)
    return render_to_response(template, locals(), RequestContext(request))
