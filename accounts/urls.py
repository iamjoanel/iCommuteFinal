from django.conf.urls import (patterns, url)
from django.contrib.auth.decorators import login_required

from route.views import (PublicDeletePathView, PublicDeleteTrainPathView, PublicDeleteRouteView)


urlpatterns = patterns('',
)

urlpatterns += patterns('route.views',
    url(r'^$', 'public_route_home', name="public_route_home"),
    url(r'^add_route/$', 'public_add_route', name="public_add_route"),
    url(r'^edit_route/(?P<pk>\d+)/$', 'public_edit_route', name="public_edit_route"),
    url(r'^delete_route/(?P<pk>\d+)/$', login_required(PublicDeleteRouteView.as_view()), name="public_delete_route"),

    url(r'^p/$', 'public_path_home', name="public_path_home"),
    url(r'^p/add_path/$', 'public_add_path', name="public_add_path"),
    url(r'^p/edit_path/(?P<pk>\d+)/$', 'public_edit_path', name="public_edit_path"),
    url(r'^p/delete_path/(?P<pk>\d+)/$', login_required(PublicDeletePathView.as_view()), name="public_delete_path"),

    url(r'^tp/$', 'public_train_path_home', name="public_train_path_home"),
    url(r'^tp/add_train_path/$', 'public_add_train_path', name="public_add_train_path"),
    url(r'^tp/edit_train_path/(?P<pk>\d+)/$', 'public_edit_train_path', name="public_edit_train_path"),
    url(r'^tp/delete_train_path/(?P<pk>\d+)/$', login_required(PublicDeleteTrainPathView.as_view()), name="public_delete_train_path"),
)
