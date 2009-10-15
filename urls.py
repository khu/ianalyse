from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import settings


urlpatterns = patterns('',
    # Example:
    # (r'^ianalyse/', include('ianalyse.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^analyse/$',                          'ianalyse.analyse.views.index'),
    (r'^analyse/(?P<build_name>\s+)/$',      'ianalyse.analyse.views.detail'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/twer/Workspace/ianalyse/media', 'show_indexes': True})
)



