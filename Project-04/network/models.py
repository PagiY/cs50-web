from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id   = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name="poster")
    text = models.CharField(max_length = 128)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default = 0)
    user_likes = models.ManyToManyField(User, blank = True)
    
    def __str__(self):
        return f"{self.id} | {self.user} posted: '{self.text}' at {self.timestamp}"
    
        
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'liked_post')