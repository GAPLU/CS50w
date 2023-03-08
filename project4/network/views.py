from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import User, Post


def index(request):
    
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    posts_list = [post.serialize() for post in posts]
    p = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def create_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    body = data.get("body", "")
    post = Post(body=body, user=request.user)
    post.save()

    return JsonResponse({"message": "Posted successfully."}, status=201)


def all_posts(request):

    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    posts_list = [post.serialize() for post in posts]
    return JsonResponse(posts_list, safe=False)


def user_profile(request, username):

    user = User.objects.get(username=username)  
    state=''
    user_req = User.objects.get(username=request.user)
    posts = user.posts.all()
    posts = posts.order_by("-timestamp").all()
    posts_list = [post.serialize() for post in posts]
    p = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    if request.method == "POST":
        if "to-follow" in request.POST:
            if not user in user_req.following.all():
                user_req.following.add(user)
        elif "to-unfollow" in request.POST:
            user_req.following.remove(user)
    
    following = user.following.count()
    followers = user.followers.count()
    if user in user_req.following.all():
        state = 'following'
    else:
        state = 'not_following'


    return render(request, "network/profile.html", {
        "UserProfile": user,
        "following": following,
        "followers": followers,
        "state": state,
        "posts": posts
    })
    

def user_posts(request, username):

    user = User.objects.get(username=username)
    posts = user.posts.all()
    posts = posts.order_by("-timestamp").all()
    posts_list = [post.serialize() for post in posts]
    p = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    return render(request, "network/profile.html", {
        "posts": posts
    })

def following_posts(request):
    
    user = User.objects.get(id=request.user.id)
    following = user.following.all()
    posts = Post.objects.filter(user__in=following).order_by("-timestamp")
    posts_list = [post.serialize() for post in posts]
    return JsonResponse(posts_list, safe=False)


def following(request):

    user = User.objects.get(id=request.user.id)
    following = user.following.all()
    posts = Post.objects.filter(user__in=following).order_by("-timestamp")
    posts_list = [post.serialize() for post in posts]
    p = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    return render(request, "network/following.html", {
        "posts": posts
    })
