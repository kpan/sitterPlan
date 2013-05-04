from django.http import HttpResponse

from spdatabase.models import ParentUser, SitterUser, Job
	
def contacts(request, username):
	try:
		s = SitterUser.objects.get(username=username)
		contacts = [p.username + ' (' + p.name + ')' for p in s.parentContacts.all()]
		return HttpResponse("My contacts: " + ', '.join(contacts))
	except:
		return HttpResponse("Error: No sitter exists with username " + username)
