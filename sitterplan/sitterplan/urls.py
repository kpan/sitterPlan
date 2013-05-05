from django.conf.urls import patterns, include, url

from spdatabase import sitterViews
from spdatabase import parentViews
from spdatabase import genericViews

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^parent/contacts/(?P<username>[^/]*)/$', parentViews.contacts, name="parentContacts"),
	url(r'^sitter/contacts/(?P<username>[^/]*)/$', sitterViews.contacts, name="sitterContacts"),
	url(r'^parent/$', parentViews.main, name="parentMain"),
	url(r'^parent/css$', parentViews.css, name="parentCss"),
	url(r'^[^/]*/genericCss$', genericViews.css, name="genericCss"),
	url(r'^[^/]*/scheduleTableJs$', genericViews.scheduleTable, name="genericScheduleTable"),
    # Examples:
    # url(r'^$', 'sitterplan.views.home', name='home'),
    # url(r'^sitterplan/', include('sitterplan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
