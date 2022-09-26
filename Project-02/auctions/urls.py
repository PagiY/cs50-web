from django.urls import path

from . import views

urlpatterns = [
    path("",                                views.index,            name="index"),
    path("login",                           views.login_view,       name="login"),
    path("logout",                          views.logout_view,      name="logout"),
    path("register",                        views.register,         name="register"),
    path("new_listing",                     views.new_listing,      name = "new_listing"),
    path("show_listing/<int:auction_id>",   views.show_listing,     name = "show_listing"),
    path("add_watchlist/<int:auction_id>",  views.add_watchlist,    name = "add_watchlist"),
    path("make_bid/<int:auction_id>",       views.make_bid,         name = "make_bid")
]
