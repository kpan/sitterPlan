from django.conf.urls import patterns, include, url

from spdatabase import sitterViews
from spdatabase import parentViews
from spdatabase import genericViews

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^parent/contacts/(?P<username>[^/]*)/$', parentViews.contacts, name="parentContacts"),
	url(r'^parent/$', parentViews.main, name="parentMain"),
	url(r'^parent/postJob$', parentViews.postJob, name="parentPost"),
	url(r'^parent/jobTable/(?P<username>[^/]*)/$', parentViews.jobTable, name="parentJobTable"),
	url(r'^parent/jobInfo/(?P<jobNumber>[^/]*)/$', parentViews.jobInfo, name="parentJobInfo"),
	url(r'^parent/deleteJob/(?P<jobNumber>[^/]*)/$', parentViews.deleteJob, name="parentDeleteJob"),
	url(r'^parent/css$', parentViews.css, name="parentCss"),
	
	url(r'^sitter/contacts/(?P<username>[^/]*)/$', sitterViews.contacts, name="sitterContacts"),
	url(r'^sitter/list$', sitterViews.jobs_list, name="sitterJobsList"),
	url(r'^sitter/calendar$', sitterViews.apply_jobs, name="sitterJobsCalendar"),
	url(r'^sitter/calendarWithJobs/$', sitterViews.calendarWithJobs, name="sitterJobsCalendarTable"),
	url(r'^sitter/schedule/(?P<username>[^/]*)/$', sitterViews.schedule, name="sitterSchedule"),
	
	url(r'^.*/sitterPlan.css$', genericViews.css, name="genericCss"),
	url(r'^.*/schedule_table.js$', genericViews.scheduleTable, name="genericScheduleTable"),
	url(r'^.*/babysitter_edit_schedule.js$', genericViews.babysitterScheduleTable, name="babysitterScheduleTable"),
    # Examples:
    # url(r'^$', 'sitterplan.views.home', name='home'),
    # url(r'^sitterplan/', include('sitterplan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
