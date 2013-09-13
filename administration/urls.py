from django.conf.urls import (patterns, url, include)
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^fare/', include('fare.urls')),
    url(r'^route/', include('route.urls')),

)

urlpatterns += patterns('administration.views',
    url(r'^login/$', 'administration_login', name="log-in"),
    url(r'^logout/$', 'administration_logout', name='administration_logout'),
)
