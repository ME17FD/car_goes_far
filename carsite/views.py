from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
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
    cars = Car.objects.filter(carname__icontains=query, occupied=0)
    if mode == 'az':
        cars = cars.order_by('carname')
    elif mode == 'za':
        cars = cars.order_by('-carname')
    elif mode == 'price':
        cars = cars.order_by('price_per_day')
    elif mode == 'pricer':
        cars = cars.order_by('-price_per_day')
    return search(cars, start, end)

def default_view(request):
    cars = list(Car.objects.filter(occupied=0))
    shuffle(cars)
    cars = cars[:12]
    
    return render(request, "index.html",{'cars' :cars})



def cars_view(request):
    query = request.GET.get('q')
    mode = request.GET.get('orderby')
    start_str =request.GET.get('start')
    start =str2datetime( start_str)
    if start_str == None: start_str = str(date.today())
    end_str = request.GET.get('end')
    end =str2datetime(end_str )
    if end_str == None: end_str = str(date.today()+timedelta(days=1))
    
    if not query:
        query = ''
    if query == None: query='' #not to search bar default 'None'

    
    cars = search_cars(query, start, end, mode)
    
    print(date.today())
    return render(request, 'carview.html',{'cars' : cars, 'query': query,
                                           'mode':mode,'start':start_str,'end':end_str,
                                           'today':str(date.today())} )

def make_request(car:Car, user:User,start:str,end:str,info:str):

    start_date = str2datetime(start)
    end_date = str2datetime(end)
    if start_date == None or end_date == None: return 'choose the start and end dates'
    if start_date > end_date: return 'wrong date format'
    if timezone.now() > start_date: return 'wrong date format'
    print(len(search([car],start,end)))
    if len(search([car],start,end))!=0:
        Car_request.objects.create(car=car, user=user,info= info,start_date = start_date,finish_date = end_date)       
        return ''
    return 'car inst available in this period, filter by search for compatible results'

def CarDetailView(request,pk):
    msg = ''
    if request.method == 'POST':
        if request.user.is_authenticated:
            
            start = request.POST['start']
            end = request.POST['end']
            info = request.POST['info']
            car = Car.objects.get(id=pk)
            user = request.user
            msg = make_request(car, user,start,end,info)
            if msg == '':
                return redirect('requests')
            
        else:
            return redirect('mylogin')
    
    car = Car.objects.get(id = pk)
    if (not car.occupied) or request.user.is_superuser or request.user.is_staff:
        return render(request, 'car_detail.html',{'car': car, 'today': str(date.today()),'error': msg })
    return HttpResponse("this car isnt available for the moment")

def car_request_view(request,request_id=None):
    if request.user.is_authenticated :
        if request.user.is_superuser or request.user.is_staff:
            if request.method == 'POST':
                specific_car_request = get_object_or_404(Car_request, pk=request_id)
                specific_car_request.accepted = request.POST.get('accepted', False) == 'on'
                specific_car_request.resolved = True
            
                specific_car_request.save()
                return redirect('requests')  # Redirect to the car request list view

            car_requests = Car_request.objects.all().order_by('-created_at')
            

            return render(request, 'car_requests_all.html', {'car_requests': car_requests})
        
        car_requests = Car_request.objects.filter(user = request.user).order_by('-created_at')
        return render(request, 'car_requests.html', {'car_requests': car_requests})
 
    else:
        return redirect('mylogin')
    
