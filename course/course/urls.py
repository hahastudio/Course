from django.conf.urls import patterns, include, url
from course.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'course.views.home', name='home'),
    # url(r'^course/', include('course.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r"^hello/$", hello),
    (r'^time/$', current_datetime),
    (r'^accounts/login/$',  login_view),
    (r'^accounts/logout/$', logout),
    (r'^teacher/profile/$', teacher_profile),
    (r'^teacher/create_course/$', create_course),
    (r'^teacher/view_course/(?P<course_id>\w{2}\d{3})/$', view_course),
    (r'^teacher/edit_course/(?P<course_id>\w{2}\d{3})/$', edit_course),
    (r'^student/profile/$', student_profile),
    (r'^student/choose_course/$', choose_course_view),
    (r'^student/choose_course/(?P<course_id>\w{2}\d{3})/$', choose_course_act),
    (r'^student/kick_course/$', kick_course_view),
    (r'^student/kick_course/(?P<course_id>\w{2}\d{3})/$', kick_course_act),
)
