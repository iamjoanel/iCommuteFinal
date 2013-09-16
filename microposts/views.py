from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .forms import MicropostForm
from accounts.views import user_panel

@login_required
def new_post(request):
    if request.method == 'POST':
        form = MicropostForm(request.POST)
        next_url = request.POST.get("next_url", "/")
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(next_url)
        else:
            return user_panel(request, form)
    return redirect('/')
