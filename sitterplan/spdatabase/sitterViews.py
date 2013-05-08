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
		contacts = [p.username + ',' + p.name for p in s.parentContacts.all()]
		return HttpResponse('\n'.join(contacts))
	except:
		return HttpResponse('Error: No sitter exists with username ' + username)

def myJobs(request, username):
	jobs = SitterUser.objects.get(username=username).jobsAccepted.all();
	output = '<colgroup><col span="1" style="width: 17%;"><col span="1" style="width: 25%;"><col span="1" style="width: 20%;"></colgroup>\n'
	for job in jobs:
		output += '<tr>\n'
		output += '<td><h2>' + job.title + '</h2><p>' + job.description + '</p></td>\n'
		output += '<td>' + job.creator.name + '</td>\n'
		output += '<td>'
		for timeRange in job.timeRanges.all():
			output += '<p>' + timeRange.startTime.strftime("%A, %x") + '</p>'
		output += '</td>\n'
		output += '<td>' 
		for timeRange in job.timeRanges.all():
			output += '<p>' + timeRange.startTime.strftime("%I%p") + '-' + timeRange.endTime.strftime("%I%p") + '</p>'
		output += '</td>\n'
		output += '<td>'
		if job.flexible:
			output += "(" + str(job.length) + " hours within this range)"
		output += '</td></tr>\n'
		
	return HttpResponse(output)

def jobApplicationPopup(request, username, jobid):
	job = Job.objects.get(id=jobid)
	output = '<h2>' + job.title + '</h2>\n'
	output += '<p>' + job.description + '</p>\n'
	output += '<table><tr><td>'
	output += '<input align="top" type="button" name="ok" value="Apply" onclick="'
	output += "$('#applyJobPopup').dialog('close'); $.get('applyForReal/" + username + "/" + str(jobid) + "/', function(data){update();});" + '"/></td>\n'
	output += '<td><input align="top" type="button" name="cancel" value="Cancel" onclick="' + "$('#applyJobPopup').dialog('close')" + '"/></td>\n'
	output += '</tr></table>'
	return HttpResponse(output)
	
def jobUnApplicationPopup(request, username, jobid):
	job = Job.objects.get(id=jobid)
	output = '<h2>' + job.title + '</h2>\n'
	output += '<p>' + job.description + '</p>\n'
	output += '<table><tr><td>'
	output += '<input align="top" type="button" name="ok" value="UnApply" onclick="'
	output += "$('#applyJobPopup').dialog('close'); $.get('unApplyForReal/" + username + "/" + str(jobid) + "/', function(data){update();});" + '"/></td>\n'
	output += '<td><input align="top" type="button" name="cancel" value="Cancel" onclick="' + "$('#applyJobPopup').dialog('close')" + '"/></td>\n'
	output += '</tr></table>'
	return HttpResponse(output)

def actuallyApplyForJob(request, username, jobid):
	job = Job.objects.get(id=jobid)
	job.applicants.add(SitterUser.objects.get(username=username))
	job.save()
	return HttpResponse("200 OK")
	
def actuallyUnApplyForJob(request, username, jobid):
	job = Job.objects.get(id=jobid)
	job.applicants.remove(SitterUser.objects.get(username=username))
	job.save()
	return HttpResponse("200 OK")

def knownJobs(request, username):
	s = SitterUser.objects.get(username=username)
	jobs = s.jobsKnownOf.all()
	output = '<colgroup><col span="1" style="width: 17%;"><col span="1" style="width: 25%;"><col span="1" style="width: 20%;"></colgroup>\n'
	for job in jobs:
		output += '<tr>\n'
		output += '<td><h2>' + job.title + '</h2><p>' + job.description + '</p></td>\n'
		output += '<td>' + job.creator.name + '</td>\n'
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
		if len(job.applicants.filter(username=username)) > 0:
			output += '<td><input type="button" class="bigButton" value="UnApply" onclick="showUnApplyJobPopup(' + str(job.id) + ')"/></td>\n</tr>\n'
		else:
			output += '<td><input type="button" class="bigButton" value="Apply" onclick="showApplyJobPopup(' + str(job.id) + ')"/></td>\n</tr>\n'
	return HttpResponse(output)
		
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
		reply += timeRange.startTime.strftime("%w %H") + " " + timeRange.endTime.strftime("%w %H") + "\n"
	return HttpResponse(reply)

def addToDict(dict, key, job, type):
	if key in dict.keys():
		dict[key].append((job, type))
	else:
		dict[key]=[(job, type)]

def goThroughJobs(jobs, dict, type):
	for job in jobs:
		for timeRange in job.timeRanges.all():
			if (timeRange.startTime + datetime.timedelta(hours=1)) >= timeRange.endTime:
				addToDict(dict, timeRange.startTime.strftime("%a%b%d%H"), job.title, type+"SingleSquare")
			else:
				addToDict(dict, timeRange.startTime.strftime("%a%b%d%H"), job.title, type+"Top")
				
				currentTime = timeRange.startTime + datetime.timedelta(hours=1)
				while currentTime < (timeRange.endTime - datetime.timedelta(hours=1)):
					addToDict(dict, currentTime.strftime("%a%b%d%H"), "&nbsp;", type+"Middle")
					currentTime = currentTime + datetime.timedelta(hours=1)
				addToDict(dict, currentTime.strftime("%a%b%d%H"), "&nbsp;", type+"Bottom")

def calendarWithJobs(request):
	dict = request.POST
	s = SitterUser.objects.get(username=dict["username"])
	st = [int(x) for x in dict["startDate"].split(" ")]
	startDate = datetime.datetime(st[0], st[1]+1, st[2])
	jobDict = {}
	goThroughJobs(s.jobsKnownOf.all(), jobDict, "available")
	goThroughJobs(s.jobsAccepted.all(), jobDict, "accepted")
	
	scheduleDict = {}
	for timeRange in s.freeTimeRanges.all():
		currentTime = timeRange.startTime
		while currentTime < timeRange.endTime:
			scheduleDict[currentTime.strftime("%w%H")] = "free"
			currentTime = currentTime + datetime.timedelta(hours=1)
	
	output = '<tr>\n<th style="width:10%;"></th>\n';
	currentDate = startDate
	for i in range(7):
		output += '<th style="width:13%;">' + currentDate.strftime("%a %d") + '</th>\n'
		currentDate = currentDate + datetime.timedelta(days=1)
	output += '</tr>\n'
	
	earliestHour = 24
	latestHour = 0
	for hour in range(0, 24):
		for day in range(0, 7):
			weeklykey = (startDate + datetime.timedelta(days=day, hours=hour)).strftime("%w%H")
			key = (startDate + datetime.timedelta(days=day, hours=hour)).strftime("%a%b%d%H")
			if weeklykey in scheduleDict.keys() or key in jobDict.keys():
				if hour < earliestHour:
					earliestHour = hour
				if hour > latestHour:
					latestHour = hour
	
	for hour in range(earliestHour, latestHour + 1):
		output += "<tr>\n<td align='right'>" + (startDate + datetime.timedelta(hours=hour)).strftime("%I%p") + "</td>"
		for day in range(0, 7):
			weeklykey = (startDate + datetime.timedelta(days=day, hours=hour)).strftime("%w%H")
			key = (startDate + datetime.timedelta(days=day, hours=hour)).strftime("%a%b%d%H")
			if weeklykey in scheduleDict.keys():
				output += "<td class='freeSquare'>"
			else:
				output += "<td class='nonfreeSquare'>"
			if key in jobDict.keys():
				joblist = jobDict[key]
				percent = 100 / len(joblist)
				for (jobtext, type) in joblist:
					output += "<div width='" + str(int(percent)) + "%' class='" + type + "'>" + jobtext + "</div>"
			output += "</td>\n"
		output += "</tr>\n"
	return HttpResponse(output)
	
	