from django.http import HttpResponse
from sitterplan.local_install_info import base_path
from spdatabase.models import ParentUser, SitterUser, Job
	
def main(request):
    file = open(base_path() + 'parent_main_page.html', 'r')
    return HttpResponse(file.read(), content_type='text/html')

def css(request):
	file = open(base_path() + 'parent_main_page.css', 'r')
	return HttpResponse(file.read(), content_type='text/css')

def contacts(request, username):
	try:
		p = ParentUser.objects.get(username=username)
		contacts = [s.username + ' (' + s.name + ')<br/>\n' for s in p.sitterContacts.all()]
		return HttpResponse(''.join(contacts))
	except:
		return HttpResponse('Error: No parent exists with username ' + username)
