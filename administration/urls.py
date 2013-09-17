from django.conf.urls import (patterns, url, include)

urlpatterns = patterns('',
    url(r'^fare/', include('fare.urls')),
    url(r'^route/', include('route.urls')),
    url(r'^requests/', include('requests.urls')),
    url(r'^feedbacks/', include('feedbacks.urls')),
)

urlpatterns += patterns('administration.views',
    url(r'^login/$', 'administration_login', name="log-in"),
    url(r'^logout/$', 'administration_logout', name='administration_logout'),
)
