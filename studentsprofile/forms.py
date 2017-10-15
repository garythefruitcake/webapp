from django import forms
from django.contrib.auth.models import User

from .models import Profile, Details


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['email', 'fname', 'mname', 'lname']


class DetailForm(forms.ModelForm):

    class Meta:
        model = Details
        fields = ['gender', 'birthday','address','profile_logo']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
