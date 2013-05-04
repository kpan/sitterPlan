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
	creator = models.ForeignKey(ParentUser, related_name="jobs")
	sitter = models.ForeignKey(SitterUser, related_name="jobsAccepted")
	applicants = models.ManyToManyField(SitterUser, related_name="jobsAppliedFor")
	
	def __unicode__(self):
		return self.title + " created by " + str(self.creator)
