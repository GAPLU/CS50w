from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comments, Watchlist, Category
from .forms import ListingForm, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(winner=None)
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['starting_bid']
            url = form.cleaned_data['image_url']
            category = form.cleaned_data['category']
            if not url:
                url = "/static/auctions/without-image.png"
            category = category.strip().lower().capitalize()
            if category:
                new_category = Category.objects.filter(category=category).first()
                if not new_category:
                    new_category = Category(category=category)
                    new_category.save()
                listing = Listing(title=title, description=description, starting_bid=bid, image_url=url, category=new_category, creator=request.user)
            else:
                listing = Listing(title=title, description=description, starting_bid=bid, image_url=url, creator=request.user)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
            
    else:           
        form = ListingForm()                
        return render(request, "auctions/create_listing.html", {
            "form": form
        })
    

@login_required
def listing(request, listing_id):
    form = Comment()                
    listing = Listing.objects.get(pk=listing_id)
    comments = reversed(listing.comments.all())
    in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing)
    if request.method == "POST":
        if request.POST.get("watchlist_add") or request.POST.get("watchlist_remove"):
            Watchlist.toggle(listing=listing, user=request.user)
            in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing)
            return render(request, "auctions/listing.html", {
                "form": form,
                "listing": listing,
                "comments": comments,
                "watchlist": in_watchlist
            })

        elif request.POST.get("new_bid"):
            bid = int(request.POST.get("bid_price"))
            if bid > listing.starting_bid:
                new_bid = Bid(listing=listing, amount=bid, user=request.user)
                new_bid.save()
                listing.starting_bid = bid
                listing.save()
                return render(request, "auctions/listing.html", {
                    "form": form,
                    "listing": listing,
                    "comments": comments,
                    "watchlist": in_watchlist
                })
            else:
                return render(request, "auctions/listing.html", {
                    "form": form,
                    "listing": listing,
                    "comments": comments,
                    "watchlist": in_watchlist,
                    "error_message": "Bid must be greater than current bid"
                })
            
        elif request.POST.get("close_auction"):
            listing.winner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        
        elif request.POST.get("add_comment"):
            filled_form = Comment(request.POST)
            if filled_form.is_valid():
                text = filled_form.cleaned_data['comment']
                comment = Comments(comment=text, listing=listing, user=request.user)
                comment.save()
                comments = reversed(listing.comments.all())
                return render(request, "auctions/listing.html", {
                    "form": form,
                    "listing": listing,
                    "comments": comments,
                    "watchlist": in_watchlist
                })

    else:              
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": form,
            "comments": comments,
            "watchlist": in_watchlist
        })


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=request.user)
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category):
    category_obj = Category.objects.filter(category=category).first() 
    listings = category_obj.listings.all()
    return render(request, "auctions/in_category.html", {
        "listings": listings 
    })