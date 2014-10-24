from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
   url(r'^$', RedirectView.as_view(url='/dispatcher/', permanent=True)),
   url(r'^dispatcher/', include('dispatcher.urls')),
   url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
   url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
   url(r'^admin/', include(admin.site.urls)),
)
