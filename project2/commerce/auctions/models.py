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
    in_watchlist = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


    def toggle_watchlist_state(self):
        if self.in_watchlist:
            self.in_watchlist = False
        else:
            self.in_watchlist = True
        self.save()

class Bid(models.Model):
    amount = models.PositiveIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
