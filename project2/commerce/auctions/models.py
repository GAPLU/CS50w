from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    image_url = models.CharField(max_length=500)
    category = models.CharField(max_length=64, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class Bid(models.Model):
    amount = models.PositiveIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    def toggle(listing, user):
        watchlist_obj = Watchlist.objects.filter(listing=listing, user=user).first()
        if watchlist_obj:
            watchlist_obj.delete()
        else:
            watchlist_obj = Watchlist(listing=listing, user=user)
            watchlist_obj.save()