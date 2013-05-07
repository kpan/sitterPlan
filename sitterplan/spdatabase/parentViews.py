import datetime
from django.http import HttpResponse
from sitterplan.local_install_info import base_path
from spdatabase.models import ParentUser, SitterUser, Job, JobTimeRange
	
def main(request):
    file = open(base_path() + 'parent_main_page.html', 'r')
    return HttpResponse(file.read(), content_type='text/html')

def css(request):
	file = open(base_path() + 'parent_main_page.css', 'r')
	return HttpResponse(file.read(), content_type='text/css')

def contacts(request, username):
	try:
		p = ParentUser.objects.get(username=username)
		contacts = [s.username + ',' + s.name for s in p.sitterContacts.all()]
		return HttpResponse('\n'.join(contacts))
	except:
		return HttpResponse('Error: No parent exists with username ' + username)

def postJob(request):
	dict = request.POST
	print dict.lists()
	j = Job.objects.create(title=dict["title"], description=dict["description"], 
						   flexible=(dict["flexible"]=="true"), length=dict["timePeriod"],
						   creator=ParentUser.objects.get(username=dict["creator"]))
	for sitter in dict.getlist("viewers[]"):
		j.viewers.add(SitterUser.objects.get(username=sitter))
	for time_string in dict.getlist("times[]"):
		t = [int(x) for x in time_string.split(" ")]
		JobTimeRange.objects.create(job=j,
									startTime=datetime.datetime(t[0], t[1]+1, t[2], t[3]), 
    								endTime=datetime.datetime(t[4], t[5]+1, t[6], t[7]))
	j.save()
	return jobTable(request, dict["creator"])
	
def jobTable(request, username):
	table = "<table id='jobTable'>\n"
	for job in ParentUser.objects.get(username=username).jobs.all():
		table += "<tr><td><a href = 'javascript:info(" + str(job.id) + ")'>" + job.title + "</a></td>\n"
		table += "<td>" + ppJobTimes(job) + "</td>\n<td>" + ppJobApplicants(job) + "</td></tr>\n"
	table += "</table>"
	return HttpResponse(table)

def jobInfo(request, jobNumber):
	job = Job.objects.get(id=jobNumber)
	info = "<h2>" + job.title + "</h2>"
	info += "<p>" + job.description + "</p>"
	info += "<center><button onclick='delJob("+jobNumber+")'>Delete Job</button></center>"
	return HttpResponse(info)
	
def deleteJob(request, jobNumber):
	job = Job.objects.get(id=jobNumber)
	creator = job.creator.username
	job.delete()
	return jobTable(request, creator)
	
def ppJobTimes(job):
	time = ""
	separator = " and<br/>"
	if job.flexible:
		time += str(job.length) + " hours within "
		separator = " or<br/>"
	
	outputstrings = []
	for timeRange in job.timeRanges.all():
		outputstrings.append(ppTimeRange(timeRange))
	return time + separator.join(outputstrings)

def ppTimeRange(timeRange):
	return timeRange.startTime.strftime("%a %b %d %I%p") + " to " + timeRange.endTime.strftime("%I%p")
	
def ppJobApplicants(job):
	if job.sitter:
		return "Hired " + str(job.sitter)
	if job.applicants.count() > 0:
		return "<a href = 'jobapplicants/" + str(job.id) + "'>" + str(job.applicants.count()) + " applicants</a>"
	return "No applicants yet"
			