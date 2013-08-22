from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static
from questions.oauth import CustomCallback
from allaccess.views import OAuthRedirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ama.views.home', name='home'),
    # url(r'^ama/', include('ama.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^', include('questions.urls')),
    
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}, name='logout'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/callback/(?P<provider>(\w|-)+)/$', CustomCallback.as_view(), name='allaccess-callback'),
    url(r'^accounts/login/(?P<provider>(\w|-)+)/$', OAuthRedirect.as_view(), name='allaccess-login'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
