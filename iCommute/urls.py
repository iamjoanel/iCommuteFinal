from django.conf.urls import (patterns, include, url)

urlpatterns = patterns('',
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/routes/', include('accounts.urls')),
    url(r'^administration/', include('administration.urls')),
    url(r'^mobile/', include('mobile.urls')),
)

urlpatterns += patterns('',
    url(r'^accounts/profile/$', 'accounts.views.user_panel', name='user_panel'),
)

urlpatterns += patterns('public.views',
    url(r'^$', 'home', name='home'),
)



urlpatterns += patterns('microposts.views',
    url(r'^report/', 'new_post', name="new_post"),
)

urlpatterns += patterns('requests.views',
    url(r'^new_requests/$', 'new_requests', name="new_requests"),
)

urlpatterns += patterns('feedbacks.views',
    url(r'^add_feedback/$', 'add_feedback', name="add_feedback"),
)

# Examples:
# url(r'^$', 'iCommute.views.home', name='home'),
# url(r'^iCommute/', include('iCommute.foo.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:
# url(r'^admin/', include(admin.site.urls)),
