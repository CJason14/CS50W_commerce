from asyncio.windows_events import NULL
from distutils.command.upload import upload
from operator import truediv
from pickle import TRUE
from pyexpat import model
from typing_extensions import Required
from unicodedata import category, decimal
from django.contrib.auth.models import AbstractUser
from django.db import models
from sqlalchemy import true


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=300)
    last_login = models.DateTimeField(null=True)
    is_superuser = models.BooleanField(null=True)
    is_staff = models.BooleanField(null=True)
    is_active = models.BooleanField(null=True)
    date_joined = models.DateField(null=True)

class Listings(models.Model):
    key = models.AutoField(primary_key=True, unique=True)
    owner = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.CharField(max_length=200, default=None, null=True)
    category = models.CharField(max_length=100, null=True, default=None)
    closed = models.BooleanField(default=False)

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    key = models.DecimalField(max_digits=100, decimal_places=0)

class Bid(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    key = models.CharField(max_length=200)
    bidder = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class CommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=200)
    context = models.CharField(max_length=1000)
    writer = models.CharField(max_length=200)