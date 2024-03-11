from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect,get_object_or_404
from .models import Car , Car_request
from django.views.generic import DetailView
from random import shuffle

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

def make_request(car, user):
    req = Car_request.objects.create(car=car, user=user)
    req.save()
    return 'saved'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'  
    context_object_name = 'car'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            car_id = self.kwargs['pk']
            car = Car.objects.get(id=car_id)
            user = request.user
            a = make_request(car, user)
            return redirect('requests')
        else:
            return redirect('mylogin')



def car_request_view(request,request_id=None):
    if request.user.is_authenticated :
        if request.user.is_superuser:
            if request.method == 'POST':
                specific_car = get_object_or_404(Car_request, pk=request_id)
                specific_car.accepted = request.POST.get('accepted', False) == 'on'
                specific_car.resolved = request.POST.get('resolved', False) == 'on'
                if specific_car.accepted:
                    specific_car.car.occupied = True
                    specific_car.car.save()
                specific_car.save()
                return redirect('requests')  # Redirect to the car request list view

            car_requests = Car_request.objects.all().order_by('-created_at')
            

            return render(request, 'car_requests_all.html', {'car_requests': car_requests})
        


        car_requests = Car_request.objects.filter(user = request.user).order_by('-created_at')
        return render(request, 'car_requests.html', {'car_requests': car_requests})
    

    
    
    else:
        return redirect('mylogin')
    
