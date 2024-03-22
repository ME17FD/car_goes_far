from traceback import print_stack
from django.http import HttpResponse
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import User
from carsite.models import Car,Car_request
from .forms import UserForm


# Create your views here.

#mylogin

def userlogin(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If authenticated, check if the user is a superuser
        if request.user.is_superuser:
            # Redirect superuser to the admin page
            return redirect('admin:index')
        
        if request.user.is_staff:
            cars = Car.objects.all()
            car_requests = Car_request.objects.all()
            return render(request, 'staff.html', {'user' : request.user, 'cars':cars,'requests':car_requests})
            

        if request.method == 'POST':
            # Logout user and redirect to the login page
            logout(request)
            return redirect('mylogin')
        # If user is authenticated and not a superuser, render logged-in page
        return render(request, 'authenticate/logged.html', {'user' : request.user})
    
    # If user is not authenticated, handle login form submission
    if request.method == 'POST':
        # Get username and password from the POST data
        username = request.POST.get("email")
        password = request.POST.get("password")
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            if user.is_superuser:
                # If the user is a superuser, redirect to admin page
                return redirect('admin:index')
            # If user is not a superuser, render logged-in page
            return render(request, 'authenticate/logged.html', {})
        else:
            # If authentication fails, render login page with error message
            return render(request, 'authenticate/login.html', {'message': 'Invalid username or password'})

    
    return render(request, 'authenticate/login.html', {})
 


def usersignup(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, 'You have successfully signed up. Please log in.')
            return redirect('mylogin')
        else:
            # If form is invalid, render the form again with error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'authenticate/register.html', {'form': form})

    else:
        form = UserForm()
    return render(request, 'authenticate/register.html', {'form': form})  

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Perform logout
        response = super().dispatch(request, *args, **kwargs)
        
        # Redirect to a specific page
        return HttpResponseRedirect(reverse_lazy('homepage'))