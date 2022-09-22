from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class List(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 1000)
    starting_price = models.FloatField()
    category = models.CharField(max_length = 64)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.BooleanField()
    
class Bid(models.Model):
    bid = models.ForeignKey(List, on_delete = models.CASCADE)
    
class Comment(models.Model):
    listing = models.ForeignKey(List, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    user_comment = models.CharField(max_length = 500)
