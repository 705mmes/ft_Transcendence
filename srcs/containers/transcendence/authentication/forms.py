from django import forms
from .models import User
from . import models


class ModifiedProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label='Username', widget=forms.TextInput(attrs={'id':'Lusername', 'class':'popuptext', 'placeholder':""}))
    password = forms.CharField(max_length=64, label='Password', widget=forms.TextInput(attrs={'id':'Password2', 'class':'popuptext', 'placeholder':"", 'type':'password'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, label='Username', widget=forms.TextInput(attrs={'id': 'username', 'class': 'popuptext', 'placeholder': ""}))
    email = forms.CharField(max_length=300, label='mail', widget=forms.TextInput(attrs={'id': 'mail', 'class': 'popuptext', 'placeholder': ""}))
    password1 = forms.CharField(max_length=64, label='Password', widget=forms.TextInput(attrs={'id': 'Password', 'class': 'popuptext', 'placeholder': "", 'type': 'password'}))
    password2 = forms.CharField(max_length=64, label='Password2', widget=forms.TextInput(attrs={'id': 'RPassword', 'class': 'popuptext', 'placeholder': "", 'type': 'password'}))

class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search Users', max_length=100)

    # def passwords_match(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    # if password1 and password2 and password2 != password1:
    #     raise forms.ValidationError("Passwords don't match")
