from django.conf.urls import patterns, url

from dispatcher import views

urlpatterns = patterns('',
                       url(r'^$', views.overview, name='overview'),
                       url(r'^alarms/$', views.alarms, name='alarms'),
                       url(r'^department/$', views.department, name='department'),
                       url(r'^loops/$', views.loops, name='loops'),
                       url(r'^contacts/$', views.contacts, name='contacts'),
                       url(r'^contacts/create/$', views.contact_create, name='contacts_create'),
                       url(r'^contacts/(?P<id>\d+)/update/$', views.contact_update, name='contacts_update'),
                       url(r'^contacts/(?P<id>\d+)/delete/$', views.contact_delete, name='contacts_delete'),
                       )
