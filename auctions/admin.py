from xml.etree.ElementTree import Comment
from django.contrib import admin

from auctions.models import Bid, Image, Listings, Watchlist, CommentModel

# Register your models here.

admin.site.register(Listings)
admin.site.register(Image)
admin.site.register(Bid)
admin.site.register(CommentModel)