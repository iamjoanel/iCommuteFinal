from django.shortcuts import (render_to_response, redirect, get_object_or_404)
from django.template import RequestContext
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .forms import RequestForm
from .models import Request


def home(request, template='requests/home.html',
         title="Request Route Management"):
    requests_list = Request.objects.all().order_by('-count')
    paginator = Paginator(requests_list, 10)

    page = request.GET.get('page')
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)

    return render_to_response(template, locals(), RequestContext(request))

@login_required
def new_requests(request, template="requests/requests-form.html",
                title="Request Route"):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)

            try:
                request_object = Request.objects.get(origin__iexact=request_instance.origin, destination__iexact=request_instance.destination)
            except Request.DoesNotExist:
                request_object = None

            if request_object is None:
                request_instance.requested_by = request.user
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
        return redirect('new_requests')
    else:
        form = RequestForm()
    return render_to_response(template, locals(), RequestContext(request))



def done(request, pk):
    requested_route = get_object_or_404(Request, pk=pk)
    message = "You Requested a Route from: %s to %s.\n is done.\n\n\n iCommute-ph Administrator " % (requested_route.origin, requested_route.destination)
    if requested_route.is_done is False:
        requested_route.is_done = True
        requested_route.save()
        send_mail("Request has been Done", message, "admin@icommute-ph.com", [requested_route.requested_by.email], fail_silently=False)
        messages.add_message(request, messages.SUCCESS, 'Route Status Updated')
        return redirect('request_home')
    else:
        requested_route.is_done = False
    return redirect('request_home')


class DeleteRequestView(DeleteView):
    model = Request
    template_name = 'requests/delete_request.html'

    def get_success_url(self):
        return reverse('request_home')
