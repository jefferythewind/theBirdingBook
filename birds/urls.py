from django.conf.urls import url

from . import views

app_name = 'birds'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^new_sighting/', views.new_sighting, name='new_sighting'),
	url(r'^edit_sighting/(?P<pk>[-\w]+)/$', views.edit_sighting, name='edit_sighting'),
	url(r'^view_sighting/(?P<pk>[-\w]+)/$', views.view_sighting.as_view(), name='view_sighting'),
	#url(r'^weather/', views.weather, name="weather"),
	url(r'^species_query/', views.species_query, name='species_query'),
]
