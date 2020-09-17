from django import forms
from models import Venue


class AddVenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ["name", "capacity"]
