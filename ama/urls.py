from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import django.templatetags.static
import django.contrib.staticfiles.templatetags.staticfiles
django.templatetags.static.static = django.contrib.staticfiles.templatetags.staticfiles.static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ama.views.home', name='home'),
    # url(r'^ama/', include('ama.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^', include('questions.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^search/', include('haystack.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.autodiscover()
