from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label='Username', widget=forms.TextInput(attrs={'id':'Lusername', 'class':'popuptext', 'placeholder':""}))
    password = forms.CharField(max_length=64, label='Password', widget=forms.TextInput(attrs={'id':'Password2', 'class':'popuptext', 'placeholder':"", 'type':'password'}))
