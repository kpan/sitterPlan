from django.http import HttpResponse
from sitterplan.local_install_info import base_path

def css(request):
	file = open(base_path() + "sitterPlan.css", 'r')
	return HttpResponse(file.read(), content_type="text/css")
	
def scheduleTable(request):
	file = open(base_path() + "schedule_table.js", 'r')
	return HttpResponse(file.read())
	
def babysitterScheduleTable(request):
	file = open(base_path() + "babysitter_edit_schedule.js", 'r')
	return HttpResponse(file.read())