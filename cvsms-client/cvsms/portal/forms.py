from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from .models import SensorDetail


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username', None)
        password = self.cleaned_data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Username or Password is incorrect")
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class AddSensorForm(forms.ModelForm):
    station_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sensor name'}))
    station_desc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sensor description'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}))

    class Meta:
        model = SensorDetail
        fields = ['station_name', 'station_desc', 'sensor_type', 'location', 'latitude', 'longitude']