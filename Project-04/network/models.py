from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime

class User(AbstractUser):
    followers = models.ManyToManyField("User", blank=True, related_name = "follower+")
    following = models.ManyToManyField("User", blank=True, related_name = "following+")

class Post(models.Model):
    id   = models.AutoField(primary_key = True)
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "poster")
    text = models.CharField(max_length = 128)
    timestamp = models.DateTimeField(auto_now_add = True)
    user_likes = models.ManyToManyField("User", blank = True, related_name="likes")
    
    # def update_time(self):
    #     self.timestamp = datetime.now()
    
    

