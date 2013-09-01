from django.shortcuts import (render_to_response, redirect, get_object_or_404)
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse


from .forms import FareForm
from .models import Fare


def add_fare(request, template="fare/fare-form.html", title="Add Fare"):
    if request.method == 'POST':
        form = FareForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Fare Added Successfully!')
            return redirect('fare_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(form.non_field_errors()))
    else:
        form = FareForm()

    return render_to_response(template, locals(), RequestContext(request))


class DeleteFareView(DeleteView):
    model = Fare
    template_name = 'fare/delete-fare.html'

    def get_success_url(self):
        return reverse('fare_home')


def edit_fare(request, fare_id, template="fare/fare-form.html", title="Edit Fare"):
    fare = get_object_or_404(Fare, pk=fare_id)

    if request.method == 'POST':
        form = FareForm(request.POST, instance=fare)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Fare Updated!')
            return redirect('fare_home')
        else:
            messages.add_message(request, messages.ERROR, ''.join(form.non_field_errors()))
    else:
        form = FareForm(instance=fare)

    return render_to_response(template, locals(), RequestContext(request))


def home(request, template="fare/home.html", title="Fare Management"):
    fares = Fare.objects.all()
    return render_to_response(template, locals(), RequestContext(request))
