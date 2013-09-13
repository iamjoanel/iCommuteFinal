from django.conf.urls import (patterns, url)

from .views import (DeletePathView, DeleteTrainPathView, DeleteRouteView)

urlpatterns = patterns('route.views',
    url(r'^$', 'route_home', name="route_home"),
    url(r'^add_route/$', 'add_route', name="add_route"),
    url(r'^edit_route/(?P<pk>\d+)/$', 'edit_route', name="edit_route"),
    url(r'^review_route/(?P<pk>\d+)/$', 'review_route', name="review_route"),
    url(r'^approve_route/(?P<pk>\d+)/$', 'approve_route', name="approve_route"),
    url(r'^delete_route/(?P<pk>\d+)/$', DeleteRouteView.as_view(), name="delete_route"),

    url(r'^path/$', 'path_home', name="path_home"),
    url(r'^path/add_path/$', 'add_path', name="add_path"),
    url(r'^path/edit_path/(?P<pk>\d+)/$', 'edit_path', name="edit_path"),
    url(r'^path/delete_path/(?P<pk>\d+)/$', DeletePathView.as_view(), name="delete_path"),

    url(r'^train_path/$', 'train_path_home', name="train_path_home"),
    url(r'^train_path/add_train_path/$', 'add_train_path', name="add_train_path"),
    url(r'^train_path/edit_train_path/(?P<pk>\d+)/$', 'edit_train_path', name="edit_train_path"),
    url(r'^train_path/delete_train_path/(?P<pk>\d+)/$', DeleteTrainPathView.as_view(), name="delete_train_path"),
)
