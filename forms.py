from django import forms
from .models import  Prediction, UserProfile, Transaction
from django.contrib.auth.models import User

class SetPrediction(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['company','day', 'nshares']

class deposit(forms.ModelForm):
    class Meta:
        model= Transaction
        fields = ['amount']


class transfer(forms.ModelForm):
    class Meta:
        model= Transaction
        fields = ['amount']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['age','initialInvestment','timeInvest','risklevel']