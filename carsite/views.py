from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from .models import Car , Car_request
from django.urls import reverse
from django.views.generic import DetailView
# Create your views here.


def default_view(request):
    
    cars = [ k for k in Car.objects.all() if not k.occupied ][:5]
    
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

def car_request_view(request):
    if request.user.is_authenticated :
        if request.user.is_superuser:
            car_requests = Car_request.objects.all()
            return render(request, 'car_requests_all.html', {'car_requests': car_requests})
        
        car_requests = Car_request.objects.filter(user = request.user)
        return render(request, 'car_requests.html', {'car_requests': car_requests})
    else:
        return redirect('mylogin')