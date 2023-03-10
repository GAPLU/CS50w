from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.urls import resolve
import json

from .models import User, Post


def posts_conf(request, type, template):

    if type == "index":
        posts = Post.objects.all()

    elif type == "following":
        user = User.objects.get(id=request.user.id)
        following = user.following.all()
        posts = Post.objects.filter(user__in=following)


    posts = posts.order_by("-timestamp").all()
    posts_list = [post.serialize() for post in posts]
    p = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    return render(request, f"network/{template}.html", {
        "posts": posts
    })
    

def index(request):

    view_name = resolve(request.path_info).url_name

    if view_name == "index":
        return posts_conf(request, "index", "index")
 
    elif view_name == "following":
        return posts_conf(request, "following", "index")
    


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
    

def update_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    body = data.get("body", "")
    id = data.get("id", "")
    Post.objects.filter(id=id).update(body=body)
    return JsonResponse({"message": "Posted successfully."}, status=201)

@csrf_exempt
def single_post(request, post_id):

    user = User.objects.get(id=request.user.id)
    post = Post.objects.filter(id=post_id).first()
    

    if post.people_like and user in post.people_like.all():
        post.people_like.remove(user)
        post.likes -= 1
    else:
        post.people_like.add(user)
        post.likes += 1

    post.save()

    return JsonResponse(post.serialize(), safe=False)
