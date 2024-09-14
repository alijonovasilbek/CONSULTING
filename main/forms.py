from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    company_code = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email','company_code', 'password1', 'password2']

# forms.py
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')