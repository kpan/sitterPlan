from django.db import models

class ParentUser(models.Model):
	username = models.CharField(max_length=30)
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.username

class SitterUser(models.Model):
	username = models.CharField(max_length=30)
	name = models.CharField(max_length=200)
	parentContacts = models.ManyToManyField(ParentUser, related_name="sitterContacts")
	
	def __unicode__(self):
		return self.username
	
class Job(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=10000)
	creator = models.ForeignKey(ParentUser, related_name="jobs")
	sitter = models.ForeignKey(SitterUser, related_name="jobsAccepted", blank="True", null="True")
	applicants = models.ManyToManyField(SitterUser, blank="True", null="True", related_name="jobsAppliedFor")
	viewers = models.ManyToManyField(SitterUser, blank="True", null="True", related_name="jobsKnownOf")
	flexible = models.BooleanField()
	length = models.IntegerField()
	
	def __unicode__(self):
		return self.title + " created by " + str(self.creator)

class JobTimeRange(models.Model):
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	job = models.ForeignKey(Job, related_name="timeRanges")

class SitterFreeTimeRange(models.Model):
	sitter = models.ForeignKey(SitterUser, related_name="freeTimeRanges")
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	
	
