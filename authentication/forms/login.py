from django import forms


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(
        min_length=8, max_length=25, widget=forms.PasswordInput
    )
    widgets = {
        'password': forms.PasswordInput(),
    }
