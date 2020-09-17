from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now as date

# from timetable import models

now = date()


class SignupForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        # validators=[validate_email],
        error_messages={"unique": "User with this email already exists"},
    )
    password = forms.CharField(
        widget=forms.PasswordInput(), min_length=6, validators=[validate_password]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), min_length=6, validators=[validate_password]
    )
    username = forms.CharField(
        widget=forms.TextInput(),
        min_length=5,
        error_messages={"unique": "Username already exists"},
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"required": True}), min_length=7
    )

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def is_email_unique(self, email):
        try:
            User.objects.get(email=email)
            raise forms.ValidationError({"email": "Email already exists"})
        except Exception:
            pass

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        password = cleaned_data.get("password", False)
        confirm_password = cleaned_data.get("confirm_password", False)

        if password != confirm_password:
            raise forms.ValidationError({"password": "Passwords do not match"})
        if User.objects.filter(email=cleaned_data.get("email", None)).count() > 1:
            raise forms.ValidationError({"email": "Email already exists"})

        return self.cleaned_data

    def save(self):
        cleaned_data = super(SignupForm, self).clean()
        user = User(
            username=cleaned_data["username"],
            email=cleaned_data["email"],
            first_name=cleaned_data["name"].split()[0],
            last_name=cleaned_data["name"].split()[0],
        )
        user.set_password(cleaned_data["password"])
        user.save()
