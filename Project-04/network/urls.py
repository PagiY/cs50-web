
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("post", views.post, name = "post"),
    path("like/<int:post_id>", views.like_post, name = "like_post"),
    path("unlike/<int:post_id>", views.unlike_post, name = "unlike_post"),
    path("profile/<int:user_id>", views.show_profile, name="show_profile"),
    path("follow/<int:user_id>", views.follow, name = "follow"),
    path("unfollow/<int:user_id>", views.unfollow, name = "unfollow"),
    path("following", views.following, name = "following"),
    
]
