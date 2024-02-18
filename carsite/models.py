from email.policy import default
from pyexpat import model
from django.db import models
from django.utils import timezone
import uuid
from django.urls import reverse

    

class Car(models.Model):
    carname = models.CharField(max_length=255)
    carburent = models.CharField(max_length=63)
    price_per_day = models.FloatField(default=0)
    plate = models.CharField( max_length=63,unique=True)
    image = models.ImageField(upload_to="media/photos/",default="media/photos/default.jpg")
    info = models.CharField(max_length=4095)
    occupied = models.BooleanField()
    id = models.UUIDField( primary_key = True, unique=True,
         default = uuid.uuid4,  editable = False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def get_absolute_url(self):
        return reverse('car-detail', kwargs={'pk': self.pk})

    
    def __str__(self):
        return f"{self.carname} {self.plate}"
    

class car_request(models.Model):
    created_at = models.DateField()
    start_date = models.DateField()
    finish_date = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField( primary_key = True, unique=True,
         default = uuid.uuid4,  editable = False)
    car_id = models.CharField(max_length = 63)
    user_id = models.CharField(max_length = 63)
    accepted = models.BooleanField(default=False)
    resolved = models.BooleanField()

    def __str__(self):
        return f"{self.created_at} request"
