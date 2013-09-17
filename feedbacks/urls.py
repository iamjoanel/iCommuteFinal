from django.conf.urls import patterns, url
from .views import DeleteFeedbackView

urlpatterns = patterns('feedbacks.views',
                       url(r'^$', 'home', name='feedback_home'),
                       url(r'^delete_feedback/(?P<pk>\d+)/$', DeleteFeedbackView.as_view(), name='delete_feedback'),
                       url(r'^approve/(?P<pk>\d+)/$', 'approve', name='approve'),
                       )
