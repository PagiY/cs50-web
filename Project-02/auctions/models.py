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
    starting_price  = models.DecimalField(decimal_places = 5, max_digits = 15)
    category        = models.CharField(max_length = 64, choices = CATEGORIES)
    user            = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "poster") 
    won_user        = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "winner", default = None, null = True, blank = True)
    status          = models.BooleanField(default = True)
    
    def __str__(self):
        return f"{self.title} \n {self.description} \n {self.starting_price} \n {self.category} \n {self.user} \n {self.status}"
    
class Bid(models.Model):
    listing         = models.ForeignKey(List, on_delete = models.CASCADE)
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    price           = models.DecimalField(decimal_places = 2, max_digits = 15, default = 0.00)
    
    def __str__(self):
        return f"{self.listing} {self.price} {self.user}" 
    
class Comment(models.Model):
    listing         = models.ForeignKey(List, on_delete = models.CASCADE)
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    user_comment    = models.CharField(max_length = 500)

    def __str__(self):
        return f"{self.listing} {self.user} {self.user_comment}"