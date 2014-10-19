from django.conf.urls import patterns, url

from dispatcher import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       )
