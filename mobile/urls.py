from django.conf.urls import (patterns, url)
from django.contrib.auth.decorators import login_required

from .views import MobileViewError


urlpatterns = patterns('mobile.views',
    url(r'^user/$', 'home', name="mobile_home"),
    url(r'^$', 'm_login', name="m_login"),
    url(r'^logout/$', 'm_logout', name='m_logout'),
    url(r'^new_report/', 'm_new_report', name="new_report"),
    url(r'^search_route/', 'm_search_route', name="m_search_route"),
    url(r'^view_route/(?P<pk>\d+)/$', 'm_view_route', name="m_view_route"),
    url(r'^view_error/$', login_required(MobileViewError.as_view()), name="m_view_error"),
    url(r'^new_requests/$', 'm_new_requests', name="m_new_requests"),
    url(r'^add_feedback/$', 'm_add_feedback', name="m_add_feedback"),
)
