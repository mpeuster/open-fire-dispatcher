from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
   url(r'^dispatcher/', include('dispatcher.urls', namespace='dispatcher')),
   url(r'^admin/', include(admin.site.urls)),
)
