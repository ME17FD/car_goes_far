from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date, timedelta
from .models import Car, Car_request
from .forms import CarForm
from .methods import str2datetime, search_cars, make_request
from django.contrib.auth import logout


def default_view(request):
    cars = Car.objects.filter(occupied=0).order_by('?')[:12]
    
    return render(request, "index.html",{'cars' :cars})



def cars_view(request):

    query = request.GET.get('q','')
    mode = request.GET.get('orderby')
    start_str =request.GET.get('start', str(date.today()))
    end_str = request.GET.get('end',str(date.today()+timedelta(days=1)))
    
    page_number = request.GET.get('page', 1)

    


    start =str2datetime( start_str)
    end =str2datetime(end_str )
    

    cars = search_cars(query, start, end, mode,page_number)

    paginator = Paginator(cars,9)
    page_obj = paginator.get_page(page_number)
    

    context = {'cars' : page_obj, 'query': query,
               'mode':mode,'start':start_str,
               'end':end_str,'today':str(date.today()),
               'page' : page_number}


    template = 'loop.html' if request.htmx else 'carview.html'
    return render(request, template, context)

def CarDetailView(request,pk):
    msg ,start ,end='',str(date.today()),str(date.today()+timedelta(days=1))    
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            
            start = request.POST['start']
            end = request.POST['end']

            car = Car.objects.get(id=pk)
            user = request.user
            made,msg = make_request(car, user,start,end)
            if made:
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
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            logout(request)
            return redirect('homepage')
        cars = Car.objects.all()
        return render(request, 'manager_page.html', {'cars': cars})
        
    return redirect('mylogin')

def add_car(request):
    if request.user.is_staff or request.user.is_superuser:
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
    return redirect('mylogin')

def edit_car(request, car_id):
    if request.user.is_staff or request.user.is_superuser:
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
    return redirect('mylogin')