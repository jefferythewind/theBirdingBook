from __future__ import unicode_literals

from django.db import models

class SpeciesFile(models.Model):
    species_list = models.FileField()

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
    species_english = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
		return self.species+" "+self.species_english

class Subspecies(models.Model):
	species = models.ForeignKey(Species)
	subspecies = models.CharField(max_length=100)

	def __str__(self):
		return self.species.species_english+" "+self.species.species+" "+self.subspecies

class Sighting(models.Model):
    caption = models.CharField(max_length=100,default=None)
    subspecies = models.ForeignKey(Subspecies, default=None, blank=True, null=True)
    species_tags = models.CharField(max_length=100,default=None, blank=True, null=True)
    lat = models.FloatField(default=None)
    lng = models.FloatField(default= None)
    #location = models.CharField(max_length=100, default=None, null=True, blank=True)
    sighting_date = models.DateTimeField()
    image = models.ImageField(default=None)
    user_id = models.IntegerField(default=None)

    def __str__(self):
        return self.caption
