from django import forms

from models import AcademicYear


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ["semester", "start_date", "end_date", "is_current"]

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get("is_current")
        data = AcademicYear.objects.filter(is_current=True).first()

        if data is not None and is_current:
            msg = "Only one academic year can be set as 'current'."
            self.add_error("is_current", msg)
