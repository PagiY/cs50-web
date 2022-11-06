from django.urls import path

from . import views

urlpatterns = [ 
    path("",                                views.index,            name = "index"),
    path("login",                           views.login_view,       name = "login"),
    path("logout",                          views.logout_view,      name = "logout"),
    path("register",                        views.register,         name = "register"),
    path("new_listing",                     views.new_listing,      name = "new_listing"),
    path("show_listing/<int:auction_id>",   views.show_listing,     name = "show_listing"),
    path("show_watchlist",                  views.show_watchlist,    name = "show_watchlist"),
    path("add_watchlist/<int:auction_id>",  views.add_watchlist,    name = "add_watchlist"),
    path("remove_watchlist/<int:auction_id>",  views.remove_watchlist,    name = "remove_watchlist"),
    path("make_bid/<int:auction_id>",       views.make_bid,         name = "make_bid"),
    path("close_auction/<int:auction_id>",  views.close_auction,    name = "close_auction"),
    path("show_categories",                 views.show_categories,  name = "show_categories"),
    path("make_comment/<int:auction_id>",   views.make_comment,     name = "make_comment"),

]
