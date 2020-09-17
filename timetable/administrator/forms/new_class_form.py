from django import forms
from models import Class


class NewClassForm(forms.ModelForm):
    admission_year = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    completion_year = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Class
        fields = ["program", "admission_year", "completion_year", "size"]
