from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError

from .models import User

def index(request):

    return render(request, 'type_speed/index.html')


def login_view(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again"))
            return redirect('login')
    else:
        return render(request, 'type_speed/login.html', {})
    

def logout_view(request):

    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('index')


def register_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.success(request, ("Passwords Should Be The Same!"))
            return render(request, "type_speed/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.success(request, ("Username Is Already Taken!"))
            return render(request, "type_speed/register.html")
        
        login(request, user)
        return redirect('index')
    

    else:
        return render(request, "type_speed/register.html", {})
    

def profile(request):
    return render(request, "type_speed/profile.html")
