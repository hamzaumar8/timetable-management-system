from django import forms
from models import Course


class NewCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["code", "title", "credit_hours"]

    def clean(self):
        cleaned_data = super(NewCourseForm, self).clean()
        if cleaned_data.get("credit_hours", False) <= 0:
            raise forms.ValidationError(
                {"credit_hours": "Credit Hours must be creater than 0"}
            )
        return self.cleaned_data
