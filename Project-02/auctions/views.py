from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    
    if auction.user == request.user:
        can_close = True 
    else:
        can_close = False
    
    return render(request, "auctions/show_listing.html", {
        "auction"   : auction,
        "can_close" : can_close,
        "counts"    : counts,
        "bids"      : max_bid,
        "bidform"   : BidForm()
    })


def add_watchlist(request, auction_id):
    return

def make_bid(request, auction_id):
    
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            listing = List.objects.get(pk = auction_id)
            price   = form.cleaned_data["price"]
            user    = request.user
            
            max_bid     = Bid.objects.filter(listing = auction_id).aggregate(Max('price'))
            
            if max_bid["price__max"] is not None:
                if (int(price) > int(max_bid["price__max"])):
                    bid = Bid(listing = listing, user = user, price = price)
                    bid.save()
                    messages.add_message(request, messages.SUCCESS, 'Bid success!')
                else:
                    messages.add_message(request, messages.ERROR, 'Bid failed!')
            else:
                if (int(price) > int(listing.starting_price)):
                    bid = Bid(listing = listing, user = user, price = price)
                    bid.save()
                    messages.add_message(request, messages.SUCCESS, 'Bid success!')
                else:
                    messages.add_message(request, messages.ERROR, 'Bid failed!')
                
            return HttpResponseRedirect(f"/show_listing/{auction_id}")
        

def close_auction(request, auction_id):
    auction     = List.objects.get(pk = auction_id)
    auction.status = False 
    max_bid     = Bid.objects.filter(listing = auction_id).annotate(max_value = Max('price')).order_by('-max_value')[0]
    auction.won_user = max_bid.user 
    auction.save()
    

    return HttpResponseRedirect(f"/show_listing/{auction_id}")