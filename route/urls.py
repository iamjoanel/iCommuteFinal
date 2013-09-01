from django.conf.urls import (patterns, url)

from .views import DeletePathView

urlpatterns = patterns('route.views',
    url(r'^$', 'route_home', name="route_home"),

    url(r'^train_path/$', 'train_path_home', name="train_path_home"),

    url(r'^path/$', 'path_home', name="path_home"),
    url(r'^path/add_path/$', 'add_path', name="add_path"),
    url(r'^path/edit_path/(?P<pk>\d+)/$', 'edit_path', name="edit_path"),
    url(r'^path/delete_path/(?P<pk>\d+)/$', DeletePathView.as_view(), name="delete_path"),

)


