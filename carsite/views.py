from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from .models import Car , Car_request
from siteuser.models import User
from django.utils import timezone
from random import shuffle
from datetime import datetime,date,timedelta
from django.db.models import Q
from .methods import *
from django.contrib import messages
from .forms import CarForm
from django.contrib import messages
from django.core.paginator import Paginator

def default_view(request):
    cars = list(Car.objects.filter(occupied=0))
    shuffle(cars)
    cars = cars[:12]
    
    return render(request, "index.html",{'cars' :cars})



def cars_view(request):
    messages.debug(request,'test')
    query = request.GET.get('q')
    mode = request.GET.get('orderby')
    start_str =request.GET.get('start')
    page_number = request.GET.get('page', 1)

    start =str2datetime( start_str)
    if start_str == None: start_str = str(date.today())
    end_str = request.GET.get('end')
    end =str2datetime(end_str )
    if end_str == None: end_str = str(date.today()+timedelta(days=1))
    
    if not query:
        query = ''
    if query == None: query='' #not to search bar default 'None'

    cars = search_cars(query, start, end, mode)
    paginator = Paginator(cars,9)
    page_obj = paginator.get_page(page_number)
    

    context = {'cars' : page_obj, 'query': query,
               'mode':mode,'start':start_str,
               'end':end_str,'today':str(date.today()),
               'page' : page_number}


    if request.htmx:
        print("reached")
        return render(request,'loop.html', context)
    
    return render(request, 'carview.html', context)


def CarDetailView(request,pk):
    msg ,start ,end='',str(date.today()),str(date.today()+timedelta(days=1))
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            
            start = request.POST['start']
            end = request.POST['end']

            car = Car.objects.get(id=pk)
            user = request.user
            msg = make_request(car, user,start,end)
            if msg == '':
                return redirect('requests')
            
        else:
            return redirect('mylogin')
    
    car = Car.objects.get(id = pk)

    if (not car.occupied) or request.user.is_superuser or request.user.is_staff:
        return render(request, 'car_detail.html',{'car': car, 'today': str(date.today()),'error': msg, 'start':start,'end':end})
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
    
def manager_page(request):
    cars = Car.objects.all()
    return render(request, 'manager_page.html', {'cars': cars})


def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'saved')
            return redirect('manager_page')
        else:
            messages.error(request,'failed to save')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'add_car.html', {'form': form})
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    print(car.occupied)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            print('saved succ')
            return redirect('manager_page')
    

    car = get_object_or_404(Car, id=car_id)
    return render(request, 'edit_car.html', {'form': form, 'car': car})
