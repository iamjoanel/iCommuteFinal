from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^accounts/', include('registration.backends.default.urls')),
)

urlpatterns += patterns('',
    url(r'^accounts/profile/$', 'accounts.views.user_panel', name='user_panel'),
)
# Examples:
# url(r'^$', 'iCommute.views.home', name='home'),
# url(r'^iCommute/', include('iCommute.foo.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:
# url(r'^admin/', include(admin.site.urls)),
