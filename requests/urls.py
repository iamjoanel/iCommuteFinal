from django.conf.urls import patterns, url

from .views import DeleteRequestView


urlpatterns = patterns('requests.views',
    url(r'^$', 'home', name='request_home'),
    url(r'^delete_request/(?P<pk>\d+)/$', DeleteRequestView.as_view(), name='delete_request'),
    url(r'^request_done/(?P<pk>\d+)/$', 'done', name='request_done')
)
