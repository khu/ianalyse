from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import settings
from analyse.config import Configs
from analyse import views

urlpatterns = patterns('',
                       
                       url(r'^analyse/$',                             views.home,  name="home"),
                       url(r'^analyse/index.html',                    views.index, name="index"),
                       url(r'^analyse/setup.html',                    views.setup, name="setup"),
                       url(r'^analyse/show.html',                     views.show,  name="show"),
                       url(r'^analyse/generate.html',                 views.generate, name="generate"),
                       (r'^media/(?P<path>.*)$',                   'django.views.static.serve',
                       {'document_root': settings.MEDIA_ROOT,      'show_indexes': True}),
                       (r'^results/(?P<path>.*)$',                 'django.views.static.serve',
                       {'document_root': Configs().results_dir(),   'show_indexes': True})
        )



