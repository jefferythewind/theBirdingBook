from django.shortcuts import render
from django.views import generic
from django.utils import timezone

from .models import Sighting

class IndexView(generic.ListView):
    template_name = 'birds/index.html'
    context_object_name = 'latest_sighting_list'

    def get_queryset(self):
	"""Return the last five sightings."""
        return Sighting.objects.filter(sighting_date__lte=timezone.now()).order_by('-sighting_date')[:10]
