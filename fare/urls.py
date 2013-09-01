from django.conf.urls import (patterns, url)

from .views import DeleteFareView

urlpatterns = patterns('fare.views',
    url(r'^$', 'home', name="fare_home"),
    url(r'^add_fare/$', 'add_fare', name="add_fare"),
    url(r'^edit_fare/(?P<fare_id>\d+)/$', 'edit_fare', name="edit_fare"),
    url(r'^delete_fare/(?P<pk>\d+)/$', DeleteFareView.as_view(), {'title': "Delete Fare"}, name="delete_fare"),
)
