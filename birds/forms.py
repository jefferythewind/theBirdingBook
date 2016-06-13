from django import forms
from .models import Sighting

class SightingsForm(forms.ModelForm):
    class Meta:
        model = Sighting
        fields = ('caption','subspecies','lat','lng','sighting_date', 'image')
        widgets = {
            'caption': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'sighting_date': forms.TextInput(attrs={'class':"mdl-textfield__input"})
        }