from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = [ ('entertainment', 'Entertainment'),
               ('electronics', 'Electronics'),
               ('fashion', 'Fashion'),
               ('appliances', 'Appliances'),
               ('grocery', 'Grocery')
]

class User(AbstractUser):
    pass

class List(models.Model):
    title           = models.CharField(max_length = 64)
    description     = models.CharField(max_length = 1000)
    img_url         = models.CharField(max_length = 128, default = '')
    starting_price  = models.FloatField()
    category        = models.CharField(max_length = 64, choices = CATEGORIES)
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    status          = models.BooleanField(default = True)
    
    def __str__(self):
        return f"{self.title} \n {self.description} \n {self.starting_price} \n {self.category} \n {self.user} \n {self.status}"
    
class Bid(models.Model):
    listing         = models.ForeignKey(List, on_delete = models.CASCADE)
    
class Comment(models.Model):
    listing         = models.ForeignKey(List, on_delete = models.CASCADE)
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    user_comment    = models.CharField(max_length = 500)
