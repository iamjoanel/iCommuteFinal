from django.conf.urls import (patterns, url)


urlpatterns = patterns('mobile.views',
    url(r'^$', 'home', name="mobile_home"),
    url(r'^login/$', 'm_login', name="m_login"),
    url(r'^logout/$', 'm_logout', name='m_logout'),
)
