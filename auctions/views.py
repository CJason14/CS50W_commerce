from asyncio.windows_events import NULL
from cgi import test
from cmath import log
from importlib.resources import path
from multiprocessing import context
from turtle import title
from typing import List
from unicodedata import category
from unittest import result
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from sqlalchemy import Integer
from .forms import ImageForm
from .models import Bid, CommentModel, Listings, User, Watchlist


def index(request):
    items = Listings.objects.all()
    listings = {
    'listings': items,
    }
    return render(request, "auctions/index.html", listings)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    owner = 0
    closed = 0
    if Listings.objects.filter(owner = request.user.username, key = listing_id):
        owner = 1
    if Listings.objects.filter(key = listing_id, closed = False):
        closed = 1
    content = Listings.objects.filter(key=listing_id)
    bid = Bid.objects.filter(key = listing_id).order_by('price').last()
    comments = CommentModel.objects.filter(key = listing_id)
    listing = {
    'listing': content,
    'owner': owner,
    'closed': closed,
    'bid': bid,
    'comments': comments
    }
    return render(request, "auctions/listing.html", listing)

@login_required(login_url="/login")
def createlisting(request):
    if request.method == "POST":
        image = ImageForm(request.POST, request.FILES)
        title = request.POST["titleitem"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        if image.is_valid():
            image.save()
            img_obj = image.instance.image.url
            Listings.objects.create(

                owner = request.user.username,
                title = title,
                description = description,
                price = price,
                photo = img_obj,
                category = category
            )
            key = Listings.objects.filter(owner = request.user.username, title = title, description = description, price = price)
            Bid.objects.create(
                key = key[0].key,
                bidder = request.user.username,
                price = price
            )
            return HttpResponseRedirect(reverse("index"))
        else:
            pass
    else:
        form = ImageForm()
        return render(request, "auctions/createlisting.html", {'form': form})

@login_required(login_url="/login")
def watchlist(request):
    current_user = request.user
    if request.method == "POST":
        if not Watchlist.objects.filter(username = current_user.username, key = request.POST["key"]):
            Watchlist.objects.create(
                username = current_user.username,
                key = request.POST["key"]
            )
    items = Watchlist.objects.filter(username = current_user.username)
    num = 0
    q1 = []
    for x in items:
        q = Listings.objects.filter(key = x.key).values()
        q1.append(list(q))
        num += 1
    allitems = {
    'allitems': items,
    'all': q1
    }
    return render(request, "auctions/watchlist.html", allitems)

@login_required(login_url="/login")
def unwatchlist(request):
    current_user = request.user
    if request.method == "POST":
        Watchlist.objects.filter(username = current_user.username, key = request.POST["key"]).delete()
    return HttpResponseRedirect("/watchlist")

@login_required(login_url="/login")
def bid(request):
    if request.method == "POST":
        bid = int(request.POST["price"])
        key = request.POST["key"]
        currentprice_o = Bid.objects.filter(key = key).order_by('price').last()
        currentprice = currentprice_o.price
        if bid > int(currentprice):
            Bid.objects.create(
                key = key,
                bidder = request.user.username,
                price = bid
            )
    return HttpResponseRedirect("/listing/" + key)

@login_required(login_url="/login")
def close(request):
    if request.method == "POST":
        Listings.objects.filter(owner = request.user.username, key = request.POST["key"]).update(closed = True)
    return HttpResponseRedirect("/listing/" + request.POST["key"])

def categories(request):
    categoriesnum = Listings.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", { 'categoriesnum': categoriesnum })

def category(request, categories):
    listings = Listings.objects.filter(category = categories)
    return render(request, "auctions/category.html", {'listings': listings, 'category': categories})

@login_required(login_url="/login")
def comment(request):
    if request.method == "POST":
        username = request.user.username
        key = request.POST["key"]
        content = request.POST["content"]
        CommentModel.objects.create(
            key = key,
            context = content,
            writer = username
        )
    return HttpResponseRedirect("/listing/" + request.POST["key"])