from django.db import models

# Create your models here.
class Person(models.Model):
	national_id   = models.CharField(max_length=20, null=True, blank=True)
	#national_id   = models.CharFielf(max_length=20, primary_key=True)
	name          = models.CharField(max_length=50, null=True,blank=True)
	last_name     = models.CharField(max_length=50, null=True,blank=True)
	age           = models.IntegerField()
	origin_planet = models.CharField(max_length=99, null=True, blank=True) 
	picture_url   = models.CharField(max_length=2084, null=True, blank=True)

	def __str__(self):
		return self.name

