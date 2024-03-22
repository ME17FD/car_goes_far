# forms.py
from django.forms import ModelForm
from .models import Car

class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['carname', 'carburent', 'price_per_day', 'plate', 'image','image_2','image_3','image_4','image_5', 'info', 'occupied']
