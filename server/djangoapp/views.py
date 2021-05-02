from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, notify for invalid username or password
            messages.add_message(request, messages.WARNING, 'wrong username or password')
            return redirect('djangoapp:index')
    else:
        # if not, redirect to login page
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])

# Create a `registration_request` view to handle sign up request
def registration(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    #if it is a POST request, perform registration procedures
    elif request.method == 'POST':
    # Get user details from request.POST dictionary
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password1 = request.POST['psw1']
        password2 = request.POST['psw2']
        # Check inserted passwords match
        if not password1 == password2:
            messages.add_message(request, messages.WARNING, 'specified passwords not matching')
            return render(request, 'djangoapp/registration.html', context)
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
            print('user already exists {}, {}, {}'.format(\
                    User.first_name, User.last_name, User.username))
        except:
            # If not confirm it is a new user
            print('this is a new user {}!'.format(username))
        # If it is a new user
        if not user_exist:
            user = User.objects.create_user(username=username, \
                    first_name=firstname, \
                    last_name=lastname, \
                    password=password1)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'created a new user')
            return redirect('djangoapp:index')
        else:
            messages.add_message(request, messages.WARNING, 'inserted username already exists')
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

