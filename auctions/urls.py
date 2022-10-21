from unicodedata import name
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("unwatchlist", views.unwatchlist, name="unwatchlist"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categories>/", views.category, name="category"),
    path("comment", views.comment, name="comment")
]

