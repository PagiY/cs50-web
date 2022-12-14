from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like
from .forms import PostForm 

def index(request):
    all_posts = Post.objects.all().order_by('-timestamp')
    #liked_posts = Likes.objects.filter(user = request.user)
    
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

def unlike_post(request, post_id):
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(id = post_id)
        
        liked = Like.objects.filter(user = user, post = post)
        liked.delete()
        
        post.likes-=1 
        post.user_likes.remove(user)
        
        post.save()
        
    return HttpResponseRedirect(f"/")

def like_post(request, post_id):
    if request.method == "POST":
        user = request.user 
        post = Post.objects.get(id = post_id)
        
        post.likes+=1
        post.user_likes.add(user)
        
        new_like = Like(user = user, post = post)
        new_like.save()
        post.save()
        
    return HttpResponseRedirect(f"/")

def post(request):
    '''
        Saves new user text and user name to Post model.
    '''
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            user = request.user
            new_post = Post(user = user, 
                            text = text,
                            likes = 0)
            new_post.save()
            
    return HttpResponseRedirect(f"/")

def show_profile(request, user_id):
    user = User.objects.get(id = user_id)
    posts = Post.objects.filter(user = user).order_by('-timestamp')
    
    return render(request, "network/profile.html", {
        "user_profile": user,
        "posts": posts 
    })
    
def follow(request, user_id):
    if request.method == "POST":
        
        #user the current logged in user wants to follow
        user_to_follow = User.objects.get(id = user_id)
        
        #update user following
        user = User.objects.get(id = request.user.id)  
        user.following.add(user_to_follow)
        
        #update user_to_follow followers count
        user_to_follow.followers+=1
        
        user_to_follow.save()
        user.save()
        
    return HttpResponseRedirect(f"/")

def unfollow(request, user_id):
    
    if request.method == "POST":
        #user the current logged in user wants to follow
        user_to_follow = User.objects.get(id = user_id)
        
        #update user following
        user = User.objects.get(id = request.user.id)  
        user.following.remove(user_to_follow)
        
        #update user_to_follow followers count
        user_to_follow.followers-=1
        
        user_to_follow.save()
        user.save()
        
    return HttpResponseRedirect(f"/")

def following(request):
    
    user = User.objects.get(id = request.user.id)
    
    user_follows = user.following.all()
    
    posts = []
    for following in user_follows:
        following_posts = Post.objects.filter(user = following)
        posts.extend(following_posts)
        
    return render(request, "network/following.html", {
        "posts" : posts
    })
