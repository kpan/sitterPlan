from django.http import HttpResponse

from spdatabase.models import ParentUser, SitterUser, Job
	
def contacts(request, username):
	try:
		p = ParentUser.objects.get(username=username)
		contacts = [s.username + ' (' + s.name + ')' for s in p.sitterContacts.all()]
		return HttpResponse("My contacts: " + ', '.join(contacts))
	except:
		return HttpResponse("Error: No parent exists with username " + username)
