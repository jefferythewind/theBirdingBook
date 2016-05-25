from __future__ import unicode_literals

from django.db import models

class Order(models.Model):
	order = models.CharField(max_length=100)

	def __str__(self):
		return self.order

class Family(models.Model):
	order = models.ForeignKey(Order)
	family_scientific = models.CharField(max_length=100)
	family_english = models.CharField(max_length=100)

	def __str__(self):
		return self.family_english+" "+self.family_scientific

class Genus(models.Model):
	family = models.ForeignKey(Family)
	genus = models.CharField(max_length=100)

	def __str__(self):
		return self.genus

class Species(models.Model):
	genus = models.ForeignKey(Genus, default=None)
	species = models.CharField(max_length=100, default=None)

	def __str__(self):
		return self.species

class Subspecies(models.Model):
	species = models.ForeignKey(Species)
	subspecies = models.CharField(max_length=100)
	common_name = models.CharField(max_length=100, default=None, blank=True)

	def __str__(self):
		return self.common_name+" "+self.subspecies

class Sighting(models.Model):
        caption = models.CharField(max_length=100,default=None)
        subspecies = models.ForeignKey(Subspecies, default=None)
        lat = models.FloatField(default=None)
        lng = models.FloatField(default= None)
        sighting_date = models.DateTimeField()
        image = models.ImageField(default=None)
        user_id = models.IntegerField(default=None)

        def __str__(self):
                return self.caption
