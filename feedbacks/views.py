import json
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import FeedbackForm
from .models import Feedback


def home(request, template="feedbacks/home.html", title="Feedback Management"):

    feedback_list = Feedback.objects.all().order_by('approved')
    feedback_paginator = Paginator(feedback_list, 10)

    page = request.GET.get('page')
    try:
        feedback = feedback_paginator.page(page)
    except PageNotAnInteger:
        feedback = feedback_paginator.page(1)
    except EmptyPage:
        feedback = feedback_paginator.page(feedback_paginator.num_pages)

    return render_to_response(template, locals(), RequestContext(request))


def add_feedback(request):
    if request.method == 'POST':
        message = "Somethings Wrong with your feedback"
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            message = 'Your comment has been sent and is under administrator inspection'

    return HttpResponse(json.dumps({'message': message}))


class DeleteFeedbackView(DeleteView):
    model = Feedback
    template_name = 'feedbacks/delete_feedback.html'

    def get_success_url(self):
        return reverse('feedback_home')


def approve(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)

    if feedback.approved is False:
        feedback.approved = True
        feedback.save()
        messages.add_message(request, messages.SUCCESS, 'Feedback Approved')
        return redirect('feedback_home')
    else:
        feedback.approved = False
        feedback.save()
        messages.add_message(request, messages.ERROR, 'Feedback Disapproved')

    return redirect('feedback_home')
