from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from .models import Sighting
from django.http import HttpResponse

import urllib2
import json

from .forms import SightingsForm

from django.contrib.auth.decorators import login_required

@login_required
def new_sighting(request):
	if request.method == "POST":
		form = SightingsForm(request.POST, request.FILES)
		if form.is_valid():
			s = form.save(commit=False)
			s.user_id = request.user.id
			s.save()
			return redirect('/view_sighting/'+str(s.pk), pk=s.pk)
	else:
		form = SightingsForm()
	return render(request, 'birds/new_sighting.html', {'form': form})

class view_sighting(generic.DetailView):
	model = Sighting
	template_name = 'birds/view_sighting.html'

class IndexView(generic.ListView):
	template_name = 'birds/index.html'
	context_object_name = 'latest_sighting_list'

	def get_queryset(self):
		"""Return the last ten sightings."""
		return Sighting.objects.filter(sighting_date__lte=timezone.now()).order_by('-sighting_date')[:10]
	
# def weather(req):
# 	if 'ids' in req.GET and 'appid' in req.GET:
# 		cities = req.GET.get('ids').split(',')
# 		json_output = "["
# 		for city in cities:
# 			result = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast/city?id='+city+'&APPID='+req.GET.get("appid"))
# 			content = result.read()
# 			content_dict = json.loads(content)
# 			json_output += '{"city":"'+content_dict['city']['name']+'","desc":"'+content_dict['list'][0]['weather'][0]['description']+'","icon":"'+content_dict['list'][0]['weather'][0]['icon']+'"},'
# 
# 		return HttpResponse(json_output[:-1]+"]", content_type='application/json')
# 	else:
# 		return HttpResponse('{"error":"need to supply city and appid."}', content_type='application/json')
