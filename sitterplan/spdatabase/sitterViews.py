from django.http import HttpResponse
from sitterplan.local_install_info import base_path
from spdatabase.models import ParentUser, SitterUser, Job

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
