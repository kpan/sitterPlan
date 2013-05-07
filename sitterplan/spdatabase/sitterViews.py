import datetime
from django.http import HttpResponse
from sitterplan.local_install_info import base_path
from spdatabase.models import ParentUser, SitterUser, Job, SitterFreeTimeRange

def apply_jobs(request):
	file = open(base_path() + 'babysitter_apply_jobs.html', 'r')
	return HttpResponse(file.read(), content_type='text/html')

def jobs_list(request):
	file = open(base_path() + 'babysitter_jobs_list.html', 'r')
	return HttpResponse(file.read(), content_type='text/html')

def contacts(request, username):
	try:
		s = SitterUser.objects.get(username=username)
		contacts = [p.username + ' (' + p.name + ')<br/>\n' for p in s.parentContacts.all()]
		return HttpResponse(''.join(contacts))
	except:
		return HttpResponse('Error: No sitter exists with username ' + username)
		
def schedule(request, username):
	s = SitterUser.objects.get(username=username)
	if request.method == 'POST':
		dict = request.POST
		s.freeTimeRanges.all().delete()
		for time_string in dict.getlist("times[]"):
			t = [int(x) for x in time_string.split(" ")]
			SitterFreeTimeRange.objects.create(sitter=s,
											   startTime=datetime.datetime(t[0], t[1]+1, t[2], t[3]), 
											   endTime=datetime.datetime(t[4], t[5]+1, t[6], t[7]))
	reply = ""
	for timeRange in s.freeTimeRanges.all():
		reply += timeRange.startTime.strftime("%a %b %d %H") + " " + timeRange.endTime.strftime("%a %b %d %H") + "\n"
	return HttpResponse(reply)