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
	output = "<table id='jobTable'>\n"
	for job in ParentUser.objects.get(username=username).jobs.all():
		output += '<tr>\n'
		output += '<td><button class="bigButton" onclick="delJob('+str(job.id)+')">Delete</button></td>' 
		output += '<td><h2>' + job.title + '</h2><p>' + job.description + '</p></td>\n'
		output += '<td>'
		for timeRange in job.timeRanges.all():
			output += '<p>' + timeRange.startTime.strftime("%A, %x") + '</p>'
		output += '</td>\n'
		output += '<td>' 
		for timeRange in job.timeRanges.all():
			output += '<p>' + timeRange.startTime.strftime("%I %p") + ' - ' + timeRange.endTime.strftime("%I %p") + '</p>'
		output += '</td>\n'
		output += '<td>'
		if job.flexible:
			output += "(" + str(job.length) + " hours within this range)"
		output += '</td>'
		output += '<td>' + ppJobApplicants(job) + '</td>' 
	output += "</table>"
	return HttpResponse(output)
	
def deleteJob(request, jobNumber):
	job = Job.objects.get(id=jobNumber)
	creator = job.creator.username
	job.delete()
	return jobTable(request, creator)

def hire(request, jobNumber, sitter):
	job = Job.objects.get(id=jobNumber)
	job.sitter = SitterUser.objects.get(username=sitter)
	print job.sitter
	job.viewers.clear()
	job.applicants.clear()
	job.save()
	return jobTable(request, job.creator.username)
	
def ppJobApplicants(job):
	if job.sitter:
		return "Hired " + str(job.sitter)
	if job.applicants.count() > 0:
		list = ""
		for applicant in job.applicants.all():
			list += "<p><a href = 'javascript:$.get(" + '"hire/' + str(job.id) + '/' + applicant.username + '/");' + "'>Hire " + applicant.name + "</a>"
		return list
	return "No applicants yet"
			