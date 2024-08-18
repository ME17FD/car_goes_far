from .models import Car, Car_request
from siteuser.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models import QuerySet,Q

def str2datetime(date_str: str) -> datetime:
    """
    Converts a string to a timezone-aware datetime object.
    """
    if date_str == None:
        return datetime.today().replace(hour=11, minute=0, tzinfo=timezone.get_current_timezone())
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(hour=11, minute=0, tzinfo=timezone.get_current_timezone())
    except ValueError:
        raise ValueError("Invalid date format, should be YYYY-MM-DD")

def search(cars: QuerySet[Car], start: datetime, end: datetime) -> QuerySet[Car]:
    """
    Filters the cars that are available between the given start and end dates.
    """
    if start > end:
        start,end = end,start
    
    available_car_ids = []
    for car in cars:
        overlapping_requests = Car_request.objects.filter(car=car).filter(
            Q(start_date__range=(start, end)) |
            Q(finish_date__range=(start, end)) |
            (Q(start_date__lte=start) & Q(finish_date__gte=end))
        )
        if not overlapping_requests.exists():
            available_car_ids.append(car.id)

    return cars.filter(id__in=available_car_ids)

def search_cars(query: str, start: datetime, end: datetime, mode: str,page_number) -> QuerySet[Car]:
    """
    Searches for cars based on a query, availability dates, and ordering mode.
    """
    cars = Car.objects.filter(carname__icontains=query, occupied=False)
    ordering_modes = {
        'az': 'carname',
        'za': '-carname',
        'price': 'price_per_day',
        'pricer': '-price_per_day'
    }

    if mode in ordering_modes:
        cars = cars.order_by(ordering_modes[mode])
    else:
        cars = cars.order_by('carname')
    return search(cars, start, end)

def make_request(car: Car, user: User, start: str, end: str)-> tuple[bool,str] :
    """
    Makes a request for a car if it's available for the specified dates.

    Args:
        car (Car): The car object to request.
        user (User): The user making the request.
        start (str): The start date of the request in ISO format.
        end (str): The end date of the request in ISO format.

    Returns:
        Tuple[bool, str]
    """
      
    try:
        start_date = str2datetime(start)
        end_date = str2datetime(end)
    except ValueError as e:
        return False,str(e)

    if start_date > end_date:
        return False,'Start date must be before end date'
    
    if timezone.now() > start_date:
        return False,'Start date cannot be in the past'

    if search(Car.objects.filter(id=car.id), start_date, end_date).exists():
        Car_request.objects.create(car=car, user=user, start_date=start_date, finish_date=end_date)
        return True, 'request sent'
    return False ,'Car is not available in this period, filter by search for compatible results'
