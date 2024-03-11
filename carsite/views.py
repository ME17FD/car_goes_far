from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect,get_object_or_404
from .models import Car , Car_request
from django.utils import timezone
from django.views.generic import DetailView
from random import shuffle
from datetime import datetime

# Create your views here.


def default_view(request):
    
    cars = list(Car.objects.filter(occupied=0))
    shuffle(cars)
    cars = cars[:12]
    
    return render(request, "index.html",{'cars' :cars})



def cars_view(request):
    
    query = request.GET.get('q')
    
    if query:
        cars = Car.objects.filter(carname__icontains=query, occupied=0)

    else:
        # If no search query, return all available cars
        cars = Car.objects.filter(occupied=0)
        
    if query == None: query='' #not to search bar default 'None'


    return render(request, 'carview.html',{'cars' : cars, 'query': query})

def make_request(car, user,start:str,end:str,info:str):
    s = start.split('-')
    f = end.split('-')
    start_date = datetime(int(s[0]),int(s[1]),int(s[2]),11,0,0,0,timezone.get_current_timezone())
    end_date =datetime(int(f[0]),int(f[1]),int(f[2]),11,0,0,0,timezone.get_current_timezone())

    Car_request.objects.create(car=car, user=user,info= info,start_date = start_date,finish_date = end_date)
    
    return 'saved'

def CarDetailView(request,pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            
            start = request.POST['start-date']
            end = request.POST['end-date']
            info = request.POST['info']
            car = Car.objects.get(id=pk)
            user = request.user
            make_request(car, user,start,end,info)
            return redirect('requests')
        else:
            return redirect('mylogin')
    
    car = Car.objects.get(id = pk)
    if (not car.occupied) or request.user.is_superuser or request.user.is_staff:
        return render(request, 'car_detail.html',{'car': car})
    return HttpResponse("this car isnt available for the moment")

def car_request_view(request,request_id=None):
    if request.user.is_authenticated :
        if request.user.is_superuser:
            if request.method == 'POST':
                specific_car_request = get_object_or_404(Car_request, pk=request_id)
                specific_car_request.accepted = request.POST.get('accepted', False) == 'on'
                specific_car_request.resolved = True
                if specific_car_request.accepted:
                    specific_car_request.car.occupied = True
                    specific_car_request.car.save()
                specific_car_request.save()
                return redirect('requests')  # Redirect to the car request list view

            car_requests = Car_request.objects.all().order_by('-created_at')
            

            return render(request, 'car_requests_all.html', {'car_requests': car_requests})
        


        car_requests = Car_request.objects.filter(user = request.user).order_by('-created_at')
        return render(request, 'car_requests.html', {'car_requests': car_requests})
    

    
    
    else:
        return redirect('mylogin')
    
