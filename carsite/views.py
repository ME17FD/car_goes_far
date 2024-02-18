from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from .models import Car
from django.urls import reverse
from django.views.generic import DetailView
# Create your views here.


def default_view(request):
    
    cars = [ k for k in Car.objects.all() if not k.occupied ][:5]
    print(type(Car.objects.all()))
    return render(request, "index.html",{'cars' :cars})



def cars_view(request):
    
    cars = [ k for k in Car.objects.all() if not k.occupied ] 
    print(cars)
    
    return render(request, 'carview.html',{'cars' : cars})

def make_request(car_id,user_id):
    pass



class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'  
    context_object_name = 'car'
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            car_id =  self.kwargs['pk']
            user_id = request.user.id 
            make_request(car_id,user_id)
            return render(request,'car_detail_requested.html')
        else:
            return redirect('mylogin')
        