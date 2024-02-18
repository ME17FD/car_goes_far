import random,os,string

from carsite.models import Car
from django.core.files import File


az = string.ascii_letters
def get_plate(a=10):
    return ''.join(random.choices(az,k=a))

a = os.listdir('random_cars').copy()
def cvt_to_png(directory):
    from PIL import Image

    a = os.listdir(directory).copy()
    for file in a:
        
        im = Image.open(str(directory)+'\\'+str(file))
        im.save(file.split('.')[0]+'.png',format='png',lossless=True)
        print(file.split('.')[0])

def oc():
    return bool(random.choices([True,False],weights=[2,8] )[0])
"""carname = models.CharField(max_length=255)
    carburent = models.CharField(max_length=63)
    price_per_day = models.FloatField()
    plate = models.CharField( max_length=63,primary_key = True,unique=True)
    image = models.ImageField(upload_to="media/photos/",default="media/photos/default.jpg")
    info = models.CharField(max_length=4095)
    occupied = models.BooleanField()"""
for file in a:
    
   

     
    
    car = Car.objects.create(carname = file.split('.')[0],carburent = random.choice(['diesel','essence']),
                             info =get_plate(50), price_per_day = random.randint(500,800),
                             occupied = oc(),plate = get_plate())
    """car.carname = file.split('.')[0]
    car.carburent = random.choice(['diesel','essence'])
    car.info = get_plate(50)
    car.price_per_day =  random.randint(500,800)
    car.occupied = random.choices([1,0],weights=[2,8] )
    car.plate = get_plate()"""


    car.image.save(file, File(open('random_cars/'+file,"rb")))
    car.save()
    print(file.split('.')[0])
    
