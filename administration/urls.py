from django.conf.urls import (patterns, url, include)
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^fare/', include('fare.urls')),
    url(r'^route/', include('route.urls')),
    url(r'^login/$', TemplateView.as_view(template_name='administration/login.html'), name="log-in"),
)

urlpatterns += patterns('administration.views',
    url(r'^administration_login/$', 'administration_login', name='administration_login'),
    url(r'^logout/$', 'administration_logout', name='administration_logout'),
)
