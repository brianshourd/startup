from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout

from views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'startup.views.home', name='home'),
    # url(r'^startup/', include('startup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', splash),
    url(r'^index.html', index),
    url(r'^accounts/register/$', register),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/login/$', auth_login),
    url(r'^courses/browse/$', browseCourses),
    url(r'^courses/(.{1,20})/$', viewCourse),
    url(r'^courses/(.{1,20})/lesson/(/d{1,2})/$', viewLesson),
    url(r'^teach/$', teach),
    url(r'^accounts/courses', myCourses),
)
