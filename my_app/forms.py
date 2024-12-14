from django import forms
from .models import Rating
from django.contrib.auth.forms import AuthenticationForm

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['password'].widget.attrs['autocomplete'] = 'off'
