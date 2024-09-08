from django import forms

from .models import TestDrive,NCar
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')

class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



class CarSearchForm(forms.Form):
    make = forms.CharField(required=False, max_length=100)
    model = forms.CharField(required=False, max_length=100)
    
class SearchForm(forms.Form):
    city = forms.CharField(required=False)
    pickup_date = forms.DateField(required=False)
    pickup_time = forms.TimeField(required=False)
    dropoff_date = forms.DateField(required=False)
    dropoff_time = forms.TimeField(required=False)
    car_type = forms.MultipleChoiceField(choices=NCar.CAR_TYPE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    passengers = forms.MultipleChoiceField(choices=NCar.PASSENGER_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    bags = forms.MultipleChoiceField(choices=NCar.BAG_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)   