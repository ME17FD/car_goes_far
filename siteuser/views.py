from traceback import print_stack
from django.http import HttpResponse
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import User
from .forms import MyCinForm


# Create your views here.

#mylogin
def userlogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    print('admin logged')
                    return redirect('/admin/')
                login(request, user)
                
                return render(request, 'authenticate/logged.html',{})
            else:
                # Return an 'invalid login' error message.
                
                return render(request, 'authenticate/login.html',{'message': 'invalid username or password'})
        else:    
            return render(request, 'authenticate/login.html',{})
    else:
            if request.user.is_superuser:
                print('admin logged')
                return redirect('/admin/')
            if request.method == 'POST':
                logout(request)
                return redirect('mylogin')

            return render(request, 'authenticate/logged.html',{})


def userlogin(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If authenticated, check if the user is a superuser
        if request.user.is_superuser:
            # Redirect superuser to the admin page
            return redirect('admin:index')

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

    # If request method is GET, render the login page
    return render(request, 'authenticate/login.html', {})
 


def usersignup(request):
    if request.method == 'POST':
        form = MyCinForm(request.POST,request.FILES)
        form = MyCinForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')  # Get password from form
            user.set_password(password)  # Hash the password
            user.save()  # Save the user object
            print('user saved')
            return redirect('mylogin')  # Redirect to a success page
        else:
            return render(request, 'authenticate/register.html',{'msg': 'error'})

    else:
        form = MyCinForm()
    return render(request, 'authenticate/register.html',{'form': form})
    

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Perform logout
        response = super().dispatch(request, *args, **kwargs)
        
        # Redirect to a specific page
        return HttpResponseRedirect(reverse_lazy('homepage'))