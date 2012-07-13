from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to
from website import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# Generic views
urlpatterns = patterns('',
        url(r'^s/(?P<path>.*)$', 'django.views.static.serve', 
             { 'document_root': settings.STATIC_ROOT, }),
        url(r'^home/$', views.get_home, name='home'),
        url(r'^revolution/$', views.get_revolution, name='revolution'),
        url(r'^timeline/$', views.get_image, name='timeline'),
        url(r'^data/$', views.get_data)
)
