import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
from .forms import PostForm 

def index(request):
    
    all_posts = Post.objects.all().order_by('-timestamp')
    
    return render(request, "network/index.html", {
        "form": PostForm(),
        "all_posts": all_posts
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

def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            user = request.user
            new_post = Post(user = user, 
                            text = text)
            new_post.save()
        return HttpResponseRedirect(reverse("index"))
    
    elif request.method == "PUT":
        
        
        data = json.loads(request.body)
        
        if data["type"] == "edit":
            post = Post.objects.get(id = data["post_id"])
            post.text = data["text"]
            post.save()
            
            return HttpResponseRedirect(reverse("index"))
        
        elif data["type"] == "like":
            
            post = Post.objects.get(id = data["post_id"])
            user = request.user 
            if user in post.user_likes.all():
                post.user_likes.remove(user)
            else:
                post.user_likes.add(user)
                
            post.save()
            
            return HttpResponseRedirect(reverse("index"))
    else:
        
        return JsonResponse({
            "error": "Invalid HTTP request."
        }, status = 400)


def following(request):
    
    user = User.objects.get(id = request.user.id)
    
    user_follows = user.following.all()
    
    posts = []
    for following in user_follows:
        following_posts = Post.objects.filter(user = following)
        posts.extend(following_posts)
        
    return render(request, "network/following.html", {
        "all_posts" : posts
    })
    

def profile(request, id):
    
    if request.method == "GET":
        
        user_profile = User.objects.get(id = id)
        
        followers = user_profile.followers.all()
        if request.user in followers:
            following = True 
        else:
            following = False 
        
        follower_count = followers.count()
        following_count = user_profile.following.all().count()
        
        posts = Post.objects.filter(user = user_profile).order_by("-timestamp")
        
        return render(request, "network/profile.html",{
            "profile_user": user_profile,
            "all_posts"   : posts,
            "following"   : following,
            "follower_count":follower_count,
            "following_count": following_count
        })
        
    elif request.method == "POST":
        
        user_profile = User.objects.get(id = id)
        user = User.objects.get(id = request.user.id)
        
        if request.user in user_profile.followers.all():
            user_profile.followers.remove(user)
            user.following.remove(user_profile)
        else:
            user_profile.followers.add(user)
            user.following.add(user_profile)
            
        user_profile.save()
        user.save() 
            
        return HttpResponseRedirect(reverse("profile", kwargs={'id' : id}))
    else:
        return JsonResponse({
            "error": "Invalid HTTP request."
        }, status = 400)
    