from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, List, Bid
from .forms import ListForm, BidForm


def index(request):
    auction_listings = List.objects.all()
    return render(request, "auctions/index.html", {
        "auction_listings":auction_listings
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

def new_listing(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            title           = form.cleaned_data["title"]
            description     = form.cleaned_data["description"]
            img_url         = form.cleaned_data["img_url"]
            starting_price  = form.cleaned_data["starting_price"]
            category        = form.cleaned_data["category"]
            user            = request.user
            
            listing = List(title = title, 
                           description = description, 
                           img_url = img_url,
                           starting_price = starting_price,
                           category = category,
                           user = user)
            listing.save()

    return render(request, "auctions/new_listing.html", {
        "form": ListForm()
    })

@login_required(login_url = 'login')
def show_listing(request, auction_id):
    auction     = List.objects.get(pk = auction_id)
    max_bid     = Bid.objects.filter(listing = auction_id).aggregate(Max('price'))
    counts      = Bid.objects.filter(listing = auction_id).count() 
    
    #get highest bid 
    print(max_bid)
    
    return render(request, "auctions/show_listing.html", {
        "auction"   : auction,
        "counts"    : counts,
        "bids"      : max_bid,
        "bidform"   : BidForm()
    })


def add_watchlist(request, auction_id):
    return

def make_bid(request, auction_id):
    
    if request.method == "POST":
        print(request.POST)
        form = BidForm(request.POST)
        
    auction = List.objects.get(pk = auction_id)
    bids    = List.objects.get(pk = auction_id)
    
    return render(request, "auctions/show_listing.html", {
        "auction": auction,
        "bids": bids,
        "bidform": BidForm()
    })
    