from django.db import models
from django.utils import timezone
import uuid
import os
from siteuser.models import User


    

class Car(models.Model):
    carname = models.CharField(max_length=255)
    carburent = models.CharField(max_length=63)
    price_per_day = models.FloatField(default=0)
    plate = models.CharField( max_length=63,unique=True)
    image = models.ImageField(upload_to="media/photos/",default="media/photos/default.png")
    image_2 = models.ImageField(upload_to="media/photos/",blank=True)
    image_3 = models.ImageField(upload_to="media/photos/",blank=True)
    image_4 = models.ImageField(upload_to="media/photos/",blank=True)
    image_5 = models.ImageField(upload_to="media/photos/",blank=True)

    info = models.TextField()
    occupied = models.BooleanField()
    id = models.UUIDField( primary_key = True, unique=True,
         default = uuid.uuid4,  editable = False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



    def delete(self, *args, **kwargs):
        # Delete the picture file if it exists
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        
        # Call the parent class's delete method
        super(Car, self).delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.carname} {self.plate}"
    

#car rental requests meant to be seen and approved/denied by staff/admins
class Car_request(models.Model):

    created_at = models.DateTimeField(default=timezone.now  )
    start_date = models.DateTimeField(default=None,null=True)
    finish_date = models.DateTimeField(default=None,null=True)
    info = models.TextField(default='')
    days_rented = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    id = models.UUIDField( primary_key = True, unique=True,
         default = uuid.uuid4,  editable = False)
    car = models.ForeignKey(Car , on_delete=models.CASCADE)

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    
    accepted = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} requested {self.car.carname}"
    
    def save(self, *args, **kwargs):
        if self.start_date and self.finish_date:
            self.days_rented = (self.finish_date - self.start_date).days
        else:
            raise TypeError('start date and finish date must be datetime objects')
        
        self.total_price = self.days_rented * self.car.price_per_day
        return super(Car_request,self).save(*args, **kwargs)
    

