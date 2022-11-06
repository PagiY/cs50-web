from django.contrib import admin
from auctions.models import User, List, Comment, Bid, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(List)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)