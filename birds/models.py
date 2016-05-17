from __future__ import unicode_literals

from django.db import models

class Sighting(models.Model):
	species = models.CharField(max_length=200)
	location = models.CharField(max_length=100)
	sighting_date = models.DateTimeField()
	user_id = models.IntegerField(default=None)

	def __str__(self):
		return self.species
