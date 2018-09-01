from django import forms

from .login import UserLoginForm
from django.contrib.auth.models import User


class UserRegisterForm(UserLoginForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email).first()
        if u:
            raise forms.ValidationError("User with such email already exists")
        return email
