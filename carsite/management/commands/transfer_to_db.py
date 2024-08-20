from django.core.management.base import BaseCommand
import random,os,string
import time
from carsite.models import Car,Car_request
from django.core.files import File
from PIL import Image


class Command(BaseCommand):
    help = 'Transfer data from folder to database'

    def add_arguments(self, parser):
        parser.add_argument(
        "--delete_old",  # Optional argument
        action="store_true",
        default=False,  # Default to False
        help="Flag to delete old data"
        )



    def handle(self, *args, **options):
        with open('random_cars/description.txt', 'r') as file:
            content = file.read()
            car_descriptions = content.splitlines()
            
        if options.get('delete_old'):
            requests_to_delete = Car_request.objects.all()
            rq_nb = 0
            cars_to_delete = Car.objects.all()
            cr_nb = 0
            for request in requests_to_delete:
                request.delete()
                rq_nb +=1
            for del_car in cars_to_delete:
                del_car.delete(0)
                cr_nb +=1
            self.stdout.write(f'deleted {rq_nb} requests and {cr_nb} cars')

        
        def get_plate(length=10):
            return ''.join(random.choices(string.ascii_letters, k=length)).upper()

        a = os.listdir('random_cars').copy()
        
        def cvt_to_jpg(directory):
            for file in os.listdir(directory):
                ext = file.split('.')[-1].lower()
                if ext not in [ 'txt']:
                    with Image.open(os.path.join(directory, file)) as img:
                        img.convert('RGB').save(
                            os.path.join(directory, f"{os.path.splitext(file)[0]}.jpg"),
                            'JPEG',
                            quality=90
                        )
                    if ext != 'jpg':
                        os.remove(os.path.join(directory, file))

            

        cvt_to_jpg('random_cars')

        for file in os.listdir('random_cars'):
            if file.endswith('.jpg'):
                car = Car.objects.create(
                    carname=os.path.splitext(file)[0],
                    carburent=random.choice(['diesel', 'essence']),
                    info=random.choice(car_descriptions),
                    price_per_day=random.randint(20, 130) * 10,
                    occupied=False,
                    plate=get_plate()
                )

                image_path = os.path.join('random_cars', file)

                with open(image_path, "rb") as image_file:
                    car.image.save(file, File(image_file))

                car.save()
                print(car.carname)
