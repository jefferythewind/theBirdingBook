from django.conf.urls import url

from . import views

app_name = 'birds'
urlpatterns = [
	url(r'^$', views.index_view, name='index'),
	url(r'^user/(?P<pk>[-\w]+)/$', views.user, name='user'),
	url(r'^about/', views.about, name='about'),
	url(r'^new_sighting/', views.new_sighting, name='new_sighting'),
	url(r'^edit_sighting/(?P<pk>[-\w]+)/$', views.edit_sighting, name='edit_sighting'),
	url(r'^view_sighting/(?P<pk>[-\w]+)/$', views.view_sighting, name='view_sighting'),
	#url(r'^weather/', views.weather, name="weather"),
	url(r'^species_query/', views.species_query, name='species_query'),
	url(r'^new_comment/', views.new_comment, name='new_comment'),
	url(r'^get_comments/', views.get_comments, name='get_comments'),
	url(r'^get_new_comments_for_user/', views.get_new_comments_for_user, name='get_new_comments_for_user'),
	url(r'^like/', views.like, name='like'),
	url(r'^unlike/', views.unlike, name='unlike'),
	url(r'^up_vote_species/', views.up_vote_species, name='up_vote_species'),
	url(r'^down_vote_species/', views.down_vote_species, name='down_vote_species'),
	url(r'^suggest_new_species/', views.suggest_new_species, name='suggest_new_species'),
	url(r'^get_species_suggestions/', views.get_species_suggestions, name='get_species_suggestions'),
	url(r'^add_photo/', views.add_photo, name='add_photo'),
]
