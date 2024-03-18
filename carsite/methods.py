from .models import Car , Car_request
from siteuser.models import User
from django.utils import timezone
from random import shuffle
from datetime import datetime,date,timedelta
from django.db.models import Q



def str2datetime(st:str)->datetime:
    try:
        s = st.split('-')
        return datetime(int(s[0]),int(s[1]),int(s[2]),11,0,0,0,timezone.get_current_timezone())#11am
    except:
        return None



def search(cars, start: datetime, end: datetime):
    if (not start) or (not end):
        return cars
    if start > end: 
        return cars
    result_list = []
    for car in cars:
        requests = Car_request.objects.filter(car=car)
        if not requests.exists():
            result_list.append(car)
            continue
        
        overlapping = requests.filter(
            Q(start_date__range=(start, end)) |
            Q(finish_date__range=(start, end)) |
            (Q(start_date__lte=start) & Q(finish_date__gte=end))
        )
        
        if not overlapping.exists():
            result_list.append(car)
    
    return result_list

def search_cars(query, start, end, mode):
    cars = Car.objects.filter(carname__icontains=query, occupied=False)
    if mode == 'az':
        cars = cars.order_by('carname')
    elif mode == 'za':
        cars = cars.order_by('-carname')
    elif mode == 'price':
        cars = cars.order_by('price_per_day')
    elif mode == 'pricer':
        cars = cars.order_by('-price_per_day')
    return search(cars, start, end)



def make_request(car:Car, user:User,start:str,end:str):

    start_date = str2datetime(start)
    end_date = str2datetime(end)
    if start_date == None or end_date == None: return 'choose the start and end dates'
    if start_date > end_date: return 'wrong date format'
    if timezone.now() > start_date: return 'wrong date format'
    print(len(search([car],start,end)))
    if len(search([car],start,end))!=0:
        Car_request.objects.create(car=car, user=user,start_date = start_date,finish_date = end_date)       
        return ''
    return 'car inst available in this period, filter by search for compatible results'
