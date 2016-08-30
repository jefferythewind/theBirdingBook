from django import forms
from .models import Sighting

class SightingsForm(forms.ModelForm):
    class Meta:
        model = Sighting
        fields = ('caption','species_tag','lat','lng','sighting_date', 'location', 'post_text')
        widgets = {
            'caption': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'sighting_date': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            #'species_tag': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'sighting_date': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'location': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            'post_text': forms.Textarea(attrs={'class':"mdl-textfield__input", 'id':"post_text_textarea"})
        }

