from django.conf.urls import url

from . import views

app_name = 'birds'
urlpatterns = [
	url(r'^$', views.index_view, name='index'),
	url(r'^authuser/', views.authenticate_user, name='authuser'),
	url(r'^setusername/', views.setusername, name='setusername'),
	url(r'^signs3/', views.signs3, name='signs3'),
	url(r'^user/(?P<pk>[-\w]+)/$', views.user, name='user'),
	url(r'^add_avatar/', views.add_avatar, name='add_avatar'),
	url(r'^about/', views.about, name='about'),
	url(r'^privacy_policy/', views.privacy_policy, name='privacy_policy'),
	url(r'^terms_of_service/', views.terms_of_service, name='terms_of_service'),
	url(r'^new_sighting/', views.new_sighting, name='new_sighting'),
	url(r'^edit_sighting/(?P<pk>[-\w]+)/$', views.edit_sighting, name='edit_sighting'),
	url(r'^view_sighting/(?P<pk>[-\w]+)/$', views.view_sighting, name='view_sighting'),
	#url(r'^weather/', views.weather, name="weather"),
	url(r'^species_query/', views.species_query, name='species_query'),
	url(r'^new_comment/', views.new_comment, name='new_comment'),
	url(r'^get_comments/', views.get_comments, name='get_comments'),
	url(r'^get_new_notifications_for_user/', views.get_new_notifications_for_user, name='get_new_notifications_for_user'),
	url(r'^like/', views.like, name='like'),
	url(r'^unlike/', views.unlike, name='unlike'),
	url(r'^up_vote_species/', views.up_vote_species, name='up_vote_species'),
	url(r'^down_vote_species/', views.down_vote_species, name='down_vote_species'),
	url(r'^suggest_new_species/', views.suggest_new_species, name='suggest_new_species'),
	url(r'^get_species_suggestions/', views.get_species_suggestions, name='get_species_suggestions'),
	url(r'^remove_photo/', views.remove_photo, name='remove_photo'),
	url(r'^image_inspect/', views.image_inspect, name='image_inspect'),
	url(r'^star_photo/', views.star_photo, name='star_photo'),
	url(r'^accept_species_suggestion/', views.accept_species_suggestion, name="accept_species_suggestion"),
	url(r'^feedback/', views.feedback, name="feedback"),
	url(r'^map/', views.map_view, name="map"),
	url(r'^info_window/', views.info_window, name="info_window"),
	url(r'^get_map_points/', views.get_map_points, name="get_map_points"),
	url(r'^sightings_search', views.sightings_search, name="sightings_search"),
	url(r'^update_search', views.update_search_session, name="update_search"),
	url(r'^.well-known/acme-challenge/UkhVC-nEsTpRuv1r9DcGYM1gVR1Ew9BNqedHbc52Pak', views.certcode, name="certcode"),
	url(r'^robots\.txt$', views.robots, name="robots"),
	url(r'^nothanks', views.nothanks, name="nothanks")
]
