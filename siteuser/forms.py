# forms.py
from django import forms
from .models import User

class MyCinForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'fname', 'lname', 'phone', 'cin', 'cin_image','password']
