from django import forms
from datetimewidget.widgets import DateTimeWidget
from .models import Sighting

class SightingsForm(forms.ModelForm):
    class Meta:
        model = Sighting
        fields = ('caption','subspecies','lat','lng','sighting_date', 'image')
