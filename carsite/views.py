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


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'  # Adjust this to your template name
    context_object_name = 'car'
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('auth')
        else:
            return HttpResponse('no auth')
        id =  self.kwargs['pk'] 
        print(id)
        return HttpResponseRedirect(reverse('success_url_name'))