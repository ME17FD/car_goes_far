from email.policy import default
from typing import Iterable
from django.db import models
from django.utils import timezone
import uuid
from django.urls import reverse
from siteuser.models import User

    

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
    

#car rental requests meant to be seen and approved/denied by staff/admins
class Car_request(models.Model):

    created_at = models.DateTimeField(default=timezone.now  )
    start_date = models.DateTimeField(default=None,null=True)
    finish_date = models.DateTimeField(default=None,null=True)

    id = models.UUIDField( primary_key = True, unique=True,
         default = uuid.uuid4,  editable = False)
    car = models.ForeignKey(Car , on_delete=models.CASCADE)

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    
    accepted = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.created_at} request"
    

