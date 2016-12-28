from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http.response import HttpResponseBadRequest
from django.views import generic
from django.utils import timezone
from .models import Sighting, Subspecies, Comment, Like, SpeciesVote, SpeciesSuggestions, BirdPhoto, Avatar, Uid
from django.http import HttpResponse
import json
from django.db.models import Q, IntegerField, Value
from django.contrib.auth.models import User
import os
import boto3



from .forms import SightingsForm

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden

def about(request):
	return render(request, 'birds/about.html')

def privacy_policy(request):
	return render(request, 'birds/privacy_policy.html')

def terms_of_service(request):
	return render(request, 'birds/terms_of_service.html')

def user(request, pk):
	return render(request, 'birds/user.html')

def signs3(request):
	if request.is_ajax():
		S3_BUCKET = os.environ.get('AWS_STORAGE_BUCKET_NAME')
	
		file_type = "image/png"
		
		new_photo = BirdPhoto.objects.create( sighting_id = request.POST.get('sighting_id'), order = 0 )
		filename = "%s.%s" % ( new_photo.id, "png" )
		new_photo.photo = filename
		new_photo.thumbnail_url = "https://s3.amazonaws.com/birdingappsmall/%s.%s" % ( new_photo.id, "png" )
		new_photo.save()

		s3 = boto3.client('s3')
	
		presigned_post = s3.generate_presigned_post(
			Bucket = S3_BUCKET,
			Key = filename,
			Fields = {"acl": "public-read", "Content-Type": file_type},
			Conditions = [
			 	{"acl": "public-read"},
			 	{"Content-Type": file_type}
			],
			ExpiresIn = 3600
		)
		return HttpResponse(json.dumps({'data': presigned_post,'filename': filename, 'url': new_photo.photo.url, 'id': new_photo.id, 'thumbnail_url': new_photo.thumbnail_url}), content_type='application/json')

@login_required
def setusername(request):
	if request.method == "POST":
		new_username = request.POST.get("username")
		if User.objects.exclude(pk=request.user.pk).filter(username=new_username).exists():
			return render(request, 'birds/setusername.html', { 'error': 'username already exists, please choose another'})
		else:
			request.user.username = new_username
			request.user.save()
			return redirect('/user/'+str(request.user.pk), pk=request.user.pk)
	elif request.method == "GET":
		return render(request, 'birds/setusername.html')

def authenticate_user(request):
	if request.is_ajax():
		import urllib
		from jose import jwt
		from django.contrib.auth import login
		idtoken = request.POST.get('idtoken')
		target_audience = "the-birding-book"
		certificate_url = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'
		response = urllib.urlopen(certificate_url)
		certs = response.read()
		certs = json.loads(certs)
		firebase_user = jwt.decode(idtoken, certs, algorithms='RS256', audience=target_audience)
		if User.objects.filter(uid__uid=firebase_user['sub']).exists():
			user = User.objects.get(uid__uid=firebase_user['sub'])
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, user)
			return HttpResponse(json.dumps({'msg':'old_user'}), content_type='application/json')
		else:
			user = User()
			user.username = firebase_user['sub']
			user.save()
			uid = Uid.objects.create( uid = firebase_user['sub'], user = user )
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			uid.save()
			login(request, user)
			return HttpResponse(json.dumps({'msg':'new_user'}), content_type='application/json')
		
@login_required
def new_sighting(request):
	new_sighting = Sighting.objects.create(user_id = request.user.id)
	return redirect('/edit_sighting/'+str(new_sighting.id), pk=new_sighting.id)
# 	return render(request, 'birds/new_sighting.html', {'form': form, 'this_sighting': new_sighting})
	

@login_required
def edit_sighting(request, pk):
	this_sighting = get_object_or_404(Sighting, pk=pk)
	form = SightingsForm( request.POST or None, request.FILES or None, instance=this_sighting )
	if request.method == "POST":
		if this_sighting.user_id != request.user.id:
			return HttpResponseForbidden()
		if form.is_valid():
			form.save()
			return redirect('/view_sighting/'+str(pk), pk=pk)
		else:
			return render(request, 'birds/new_sighting.html', { 'form': form, 'this_sighting': this_sighting })
	elif request.method == "GET":
		return render(request, 'birds/new_sighting.html', { 'form': form, 'this_sighting': this_sighting })

def view_sighting(request, pk):
	this_sighting = get_object_or_404(Sighting, pk=pk)
	species_votes = SpeciesVote.objects.filter( sighting = this_sighting, species = this_sighting.species_tag ).count()
	if request.user.is_authenticated():
		Comment.objects.filter( sighting = this_sighting, sighting__user_id = request.user.id ).all().update(viewed_by_user = True)
		is_liked = Like.objects.filter( user = request.user, sighting = this_sighting ).count()
		is_voted = SpeciesVote.objects.filter( user = request.user, sighting = this_sighting, species = this_sighting.species_tag ).count()	
		return render(request, 'birds/view_sighting.html', { 'sighting': this_sighting, 'is_liked': is_liked, 'is_voted': is_voted,'species_votes': species_votes})
	else:
		return render(request, 'birds/view_sighting.html', { 'sighting': this_sighting, 'species_votes': species_votes})

def index_view(request):
	latest_sighting_list = Sighting.objects.filter(sighting_date__lte=timezone.now()).order_by('-post_ts')[:10]
	return render(request, 'birds/index.html', { 'latest_sighting_list': latest_sighting_list})
		
def species_query(request):
	if request.method == "GET":
		term = request.GET.get('term')
		l = list(Subspecies.objects.filter( Q(subspecies__icontains=term) | Q(species__species__icontains=term) | Q(species__species_english__icontains=term) ).order_by('subspecies')[:10])
		l2 = [{'value':unicode(i), 'id':i.pk} for i in l]
		data = json.dumps(l2)
		return HttpResponse(data, content_type='application/json')

def get_comments(request):
	if request.is_ajax():
		comments = Comment.objects.filter( sighting = request.POST.get('this_sighting') ).order_by('post_ts')
		return render_to_response('birds/comments.html', {'comments': comments})

@login_required
def get_new_comments_for_user(request):
	if request.is_ajax():
		comments = Comment.objects.filter( sighting__user_id = request.user.id, viewed_by_user = False ).order_by('-post_ts')
		return render_to_response('birds/user_comments.html', {'comments': comments})
		

@login_required
def new_comment(request):
	if request.is_ajax():
		Comment.objects.create( comment = request.POST.get('new_comment'), sighting_id = request.POST.get('sighting_id'), user_id = request.user.id )
		return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')
	
@login_required 
def like(request):
	if request.is_ajax():
		if Like.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).count() > 0:
			return HttpResponse(json.dumps({'msg':'you already liked this one'}), content_type='application/json')
		else:
			Like.objects.create( user = request.user, sighting_id = request.POST.get('sighting_id') )
			new_likes = Sighting.objects.get( pk = request.POST.get('sighting_id') ).num_likes
			return HttpResponse(json.dumps({'msg':'success', 'new_likes': new_likes}), content_type='application/json')
		
@login_required 
def unlike(request):
	if request.is_ajax():
		if Like.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).count() < 1:
			return HttpResponse(json.dumps({'msg':'you have not liked this one'}), content_type='application/json')
		else:
			Like.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).delete()
			new_likes = Sighting.objects.get( pk = request.POST.get('sighting_id') ).num_likes
			return HttpResponse(json.dumps({'msg':'success', 'new_likes': new_likes}), content_type='application/json')
		
@login_required 
def up_vote_species(request):
	if request.is_ajax():
		if SpeciesVote.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count() > 0:
			return HttpResponse(json.dumps({'msg':'you have already voted this one'}), content_type='application/json')
		else:
			SpeciesVote.objects.create(  user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') )
			new_votes = SpeciesVote.objects.filter( sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count()
			return HttpResponse(json.dumps({'msg':'success', 'new_votes': new_votes, 'species_id': request.POST.get('species_id')}), content_type='application/json')
		
@login_required 
def down_vote_species(request):
	if request.is_ajax():
		if SpeciesVote.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count() < 1:
			return HttpResponse(json.dumps({'msg':'you have not voted this one'}), content_type='application/json')
		else:
			SpeciesVote.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).delete()
			new_votes = SpeciesVote.objects.filter( sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id') ).count()
			return HttpResponse(json.dumps({'msg':'success', 'new_votes': new_votes, 'species_id': request.POST.get('species_id')}), content_type='application/json')

@login_required
def suggest_new_species(request):
	if request.is_ajax():  
		if SpeciesSuggestions.objects.filter( user = request.user, sighting_id = request.POST.get('sighting_id') ).count() > 0:
			return HttpResponse(json.dumps({'msg':'you have already suggested a species for this post'}), content_type='application/json')
		else:
			SpeciesSuggestions.objects.create( user = request.user, sighting_id = request.POST.get('sighting_id'), species_id = request.POST.get('species_id'))
			return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')

def get_species_suggestions(request):
	if request.is_ajax():
		species_suggestions = SpeciesSuggestions.objects.filter( sighting_id = request.POST.get('sighting_id') ).annotate(is_voted=Value(0, output_field=IntegerField()))
		for suggestion in species_suggestions:
			suggestion.is_voted = SpeciesVote.objects.filter( sighting_id = request.POST.get('sighting_id'), species = suggestion.species, user = request.user ).count()
		return render_to_response('birds/species_suggestions.html', {'species_suggestions': species_suggestions,'user': request.user})
	
@login_required
# def add_photo(request):
# 	if request.is_ajax():
# 		new_photo = BirdPhoto.objects.create( sighting_id = request.POST.get('sighting_id'), photo = request.POST.get('filename'), order = 0 )
# 		return HttpResponse(json.dumps({'msg':'success', 'urls': [new_photo.photo.url], 'ids': [new_photo.id]}), content_type='application/json')
	
@login_required
def remove_photo(request):
	if request.is_ajax():
		get_object_or_404(BirdPhoto, pk=request.POST.get('image_id')).delete()
		return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')
	
@login_required
def add_avatar(request):
	if request.is_ajax():
		try:
			new_avatar = request.user.avatar
		except Avatar.DoesNotExist:
			new_avatar = Avatar.objects.create( avatar = request.FILES.get('avatar_photo'), user = request.user )
		else:
			new_avatar.avatar = request.FILES.get('avatar_photo')
			new_avatar.save()
			
		return HttpResponse(json.dumps({'msg':'success', 'url': str(new_avatar.avatar.url)}), content_type='application/json')
	
@login_required
def image_inspect(request):
	if request.is_ajax():
		image = get_object_or_404(BirdPhoto, pk = request.POST.get('image_id'))
		return render_to_response('birds/image_inspect.html', {'image': image})
	
@login_required
def star_photo(request):
	if request.is_ajax():
		photo = get_object_or_404(BirdPhoto, pk = request.POST.get('image_id'))
		photo.order = 1
		photo.save()
		BirdPhoto.objects.filter(sighting = photo.sighting).exclude(pk = photo.id).update(order = 0)
		return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')
	
@login_required
def accept_species_suggestion(request):
	if request.is_ajax():
		this_sighting = get_object_or_404(Sighting, pk = request.POST.get('sighting_id') )
		this_suggestion = get_object_or_404(SpeciesSuggestions, pk = request.POST.get('suggestion_id') )
		this_sighting.species_tag = this_suggestion.species
		this_sighting.save()
		this_suggestion.delete()
		return HttpResponse(json.dumps({'msg':'success'}), content_type='application/json')

def feedback(request):
	return render(request, 'birds/feedback.html')

def map_view(request):
	sighting_data = Sighting.objects.filter(lat__isnull=False).only('lat','lng')
	return render(request, 'birds/map.html', {'sightings': sighting_data})
		
