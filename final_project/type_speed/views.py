from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
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
    tests = user.scores.all().count()
    if not tests:
        tests = 0
    scores = user.scores.filter(custom=False).order_by('-chars_min')
    return render(request, "type_speed/profile.html", {
        'scores': scores[:3],
        'tests': tests
    })


def process_results(request):
    
    if request.method == "POST":

        data = json.loads(request.body)
        words = data['words']
        spelled = data['spelled']
        accuracy = data['accuracyRate']
        custom = data['custom']
        if custom == False:
            if User.objects.filter(username=request.user):
                result = Scores(user=request.user, words_min=words, chars_min=spelled, accuracy=accuracy, custom=False)
                result.save()
            return HttpResponse(status=204)
        else:
            text_id = data['textId']
            if User.objects.filter(username=request.user):
                text = CustomText.objects.get(id=text_id)
                result = Scores(user=request.user, words_min=words, chars_min=spelled, accuracy=accuracy, custom=True, text=text)
                result.save()
            return HttpResponse(status=204)
        

def create_text(request):

    if request.method == "GET":
        if User.objects.filter(username=request.user):
            return render(request, "type_speed/text_form.html")
        else:
            return redirect('login')
    
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text-body"]
        custom_text = CustomText(user=request.user, title=title, text=text)
        custom_text.save()
        return redirect('index')


def custom(request):
            
    if User.objects.filter(username=request.user):
        texts = CustomText.objects.all()
        return render(request, 'type_speed/custom.html', {
            "texts": texts
        })
    else:
        return redirect('login')


def send_text(request, id):

    text = CustomText.objects.get(id=id)
    return JsonResponse(text.serialize(), safe=False)


def filtered(request, mode):

    if mode == "Standart" or not User.objects.filter(username=request.user):
        scores = Scores.objects.filter(custom=False).order_by('-chars_min')
        mode = "Standart"
    elif mode == "Custom":
        scores = Scores.objects.filter(custom=True).order_by('-chars_min')
    p = Paginator(scores, 10)
    page = request.GET.get('page')
    scores = p.get_page(page)
    start_rank = (scores.number - 1) * scores.paginator.per_page

    return render(request, "type_speed/ranking.html", {
        'scores': scores,
        'start_rank': start_rank,
        "mode": mode
    })    
        

def get_rank(request, chars, mode):

    rank = Scores.objects.filter(custom=mode)
    rank = rank.filter(chars_min__gt=chars).count() + 1
    return JsonResponse({"rank": rank})