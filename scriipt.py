"""
scriipt.py
used in manage.py shell with 'exec(open('scriipt.py').read())'
fills out the database with generic descriptions and the carname from the picture label

"""
import random,os,string
import time
from carsite.models import Car
from django.core.files import File
from PIL import Image
import os

car_descriptions = [
    "Sporty and sleek design, perfect for those who crave dynamic driving experiences. With its aerodynamic profile and responsive handling, this car is engineered to deliver thrills on every journey, whether it's a spirited drive through winding roads or a leisurely cruise along the coastline.",
    "Comfortable cruiser, ideal for both long journeys and daily city commutes. With its plush seating, smooth ride, and ample legroom, this car ensures that every passenger enjoys a relaxing and enjoyable travel experience. Whether you're heading out on a road trip or navigating busy city streets, comfort is always guaranteed.",
    "Spacious yet compact, offering the perfect blend of versatility and convenience for various travel needs. This car may be small in size, but it packs a surprising amount of interior space, making it suitable for everything from grocery runs to weekend getaways. With its clever storage solutions and flexible seating options, you'll find that it's always ready to adapt to your lifestyle.",
    "Stylish city runner, seamlessly blending form and function to make a statement on urban streets. With its sleek exterior design and innovative features, this car is as much a fashion accessory as it is a mode of transportation. From its eye-catching silhouette to its advanced technology, it's the perfect choice for those who want to stand out from the crowd.",
    "Adventure-ready SUV, equipped to tackle any terrain with confidence and capability. Whether you're navigating through rugged off-road trails or cruising along the highway, this car offers the versatility and performance you need for your next adventure. With its spacious interior, rugged exterior styling, and advanced off-road features, it's ready to take you wherever your wanderlust leads.",
    "Eco-friendly hybrid, combining efficiency and sustainability to reduce your carbon footprint without compromising on performance. With its innovative hybrid powertrain, this car offers impressive fuel efficiency and lower emissions, making it an environmentally conscious choice for eco-conscious drivers. Whether you're commuting to work or embarking on a road trip, you can feel good knowing that you're doing your part for the planet.",
    "Luxurious sedan, epitomizing elegance and refinement on the road. From its premium interior materials to its sophisticated exterior styling, every detail of this car exudes luxury and class. With its smooth and quiet ride, advanced technology features, and unparalleled comfort, it offers a first-class driving experience that's truly unrivaled.",
    "Family-friendly minivan, designed with the needs of busy families in mind. With its spacious interior, flexible seating arrangements, and abundance of storage space, this car provides the comfort and convenience that families crave on the go. Whether you're carpooling to soccer practice or embarking on a cross-country road trip, this minivan has you covered.",
    "Powerful and refined, this car delivers impressive performance with a touch of sophistication. From its responsive engine to its precise handling, every aspect of this car is engineered to provide an exhilarating driving experience. Whether you're accelerating on the open highway or navigating through tight city streets, you'll appreciate the power and precision that this car has to offer.",
    "Urban explorer, designed to navigate city streets with ease and agility. With its compact size, nimble handling, and advanced safety features, this car is perfectly suited for urban environments. Whether you're weaving through traffic or squeezing into tight parking spaces, you'll find that this car makes city driving a breeze.",
    "Versatile crossover, offering the best of both worlds in terms of style and utility. With its sleek exterior design and spacious interior, this car combines the comfort and convenience of a sedan with the practicality and versatility of an SUV. Whether you're running errands around town or heading out on a weekend adventure, this crossover has you covered.",
    "Classic elegance, boasting timeless design and sophistication for discerning drivers. From its graceful lines to its refined interior, this car exudes a sense of timeless beauty and luxury. Whether you're arriving at a black-tie event or cruising along scenic country roads, you'll command attention and admiration in this classic beauty.",
    "Tech-savvy commuter, equipped with advanced features to make your daily commute more enjoyable and convenient. From its intuitive infotainment system to its driver-assist technologies, this car offers a seamless blend of connectivity, safety, and entertainment options. Whether you're stuck in traffic or cruising down the highway, you'll appreciate the intelligent features that this car has to offer.",
    "Off-road adventurer, built to conquer rugged terrain with ease and confidence. With its robust construction, high ground clearance, and advanced off-road capabilities, this car is ready to take on any challenge that Mother Nature throws its way. Whether you're exploring remote trails or tackling rocky mountain passes, you can trust that this car will get you there and back again safely.",
    "Sporty hatchback, combining dynamic performance with practicality in a compact package. With its nimble handling, responsive engine, and versatile cargo space, this car offers the perfect blend of fun and functionality. Whether you're zipping around city streets or embarking on a weekend getaway, you'll enjoy the spirited driving experience that this hatchback delivers.",
    "Executive luxury, offering indulgent comfort and prestige for discerning travelers. From its opulent interior appointments to its smooth and refined ride, every aspect of this car is designed to cater to the needs of executive clientele. Whether you're chauffeuring clients to important meetings or enjoying a night out on the town, you'll appreciate the sophistication and elegance that this car exudes.",
    "Modern and efficient, featuring innovative design and engineering for a smarter driving experience. From its fuel-efficient engine to its advanced safety features, this car is engineered to deliver impressive performance and reliability on the road. Whether you're commuting to work or running errands around town, you'll appreciate the modern amenities and technology that this car has to offer.",
    "Practical and reliable, this car is a trusted companion for everyday journeys. With its dependable performance, spacious interior, and fuel-efficient engine, it's the perfect choice for drivers who value reliability and versatility. Whether you're running errands or embarking on a road trip, you can count on this car to get you where you need to go safely and efficiently.",
    "Sleek coupe, combining style and performance for a thrilling driving experience. From its aerodynamic profile to its powerful engine, every aspect of this car is designed to deliver exhilarating performance on the road. Whether you're carving up winding mountain roads or cruising along the coastline, you'll enjoy the sporty handling and dynamic acceleration that this coupe offers.",
    "All-terrain warrior, ready to conquer any challenge on and off the road. With its rugged construction, advanced four-wheel-drive system, and high ground clearance, this car is built to tackle even the toughest terrain with ease. Whether you're navigating through snow and ice or traversing rocky trails, you can trust that this car will get you through it all safely and confidently."
]


az = string.ascii_letters
def get_plate(a=10):
    return ''.join(random.choices(az,k=a))

a = os.listdir('random_cars').copy()
def cvt_to_png(directory):

    
    for file in a:
        if file.split('.')[-1] != 'png':
            im = Image.open(str(directory)+'\\'+str(file))
            im.save(directory+'/'+file.split('.')[0]+'.png',format='png',lossless=True)
            print(file.split('.')[0])
            os.remove(directory+'/'+file)

cvt_to_png('random_cars')

def oc():
    return bool(random.choices([True,False],weights=[2,8] )[0])

a = os.listdir('random_cars').copy()
def compress_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((800, 600))  # Adjust the size as needed
    img = img.convert("RGB")  # Convert image to RGB mode for JPEG format
    img.save(image_path, optimize=True, quality=80, format='JPEG')  # Save as JPEG format

time.sleep(0.5)
for file in a:
    car = Car.objects.create(
        carname=file.split('.')[0],
        carburent=random.choice(['diesel', 'essence']),
        info=random.choices(car_descriptions)[0],
        price_per_day=random.randint(20, 130) * 10,
        occupied=oc(),
        plate=get_plate()
    )

    image_path = 'random_cars/' + file
    compress_image(image_path)  # Compress the image before saving

    with open(image_path, "rb") as image_file:
        car.image.save(file, File(image_file))
    
    car.save()
    print(file.split('.')[0])
