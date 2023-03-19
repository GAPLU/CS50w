from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
import json

from .models import User, Scores, CustomText

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
        gender = request.POST.get("gender")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not email or not gender or not password or not confirmation:
            messages.success(request, ("All Fields Should Be Filled!"))
            return render(request, "type_speed/register.html")

        if password != confirmation:
            messages.success(request, ("Passwords Should Be The Same!"))
            return render(request, "type_speed/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, gender=gender)
            user.save()
        except IntegrityError:
            messages.success(request, ("Username Is Already Taken!"))
            return render(request, "type_speed/register.html")
        
        login(request, user)
        return redirect('index')
    
    else:
        return render(request, "type_speed/register.html", {})
    

def profile(request, username):

    user = User.objects.get(username=username)  
    scores = user.scores.all().order_by('-chars_min')
    return render(request, "type_speed/profile.html", {
        'scores': scores[:3]
    })


def process_results(request):
    
    if request.method == "POST":

        data = json.loads(request.body)
        words = data['words']
        spelled = data['spelled']
        accuracy = data['accuracyRate']
        if User.objects.filter(username=request.user):
            result = Scores(user=request.user, words_min=words, chars_min=spelled, accuracy=accuracy)
            result.save()
        return HttpResponse(status=204)
    

def ranking(request):
    scores = Scores.objects.all().order_by('-chars_min')
    return render(request, "type_speed/ranking.html", {
        'scores': scores
    })    


def create_text(request):

    if request.method == "GET":
        return render(request, "type_speed/text_form.html")
    
    if request.method == "POST":
        text = request.POST["text-body"]
        custom_text = CustomText(user=request.user, text=text)
        custom_text.save()
        return redirect('index')
