from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        