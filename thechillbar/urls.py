from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'thechillbar.views.home', name='home'),
    url(r'^sign$', 'thechillbar.views.sign', name='sign'),
    url(r'^login$', 'thechillbar.views.login', name='login'),
    url(r'^logout$', 'thechillbar.views.logout', name='logout'),
    url(r'^bannedips$', 'thechillbar.views.bannedips', name='bannedips'),
    url(r'^signlog$', 'thechillbar.views.signlog', name='signlog'),
    url(r'^ban$', 'thechillbar.views.ban', name='ban'),
    url(r'^unban$', 'thechillbar.views.unban', name='unban'),

    #Resources
    url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
