from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    gender = models.CharField(max_length=32, default='other')


class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores")
    words_min = models.IntegerField(default=0)
    chars_min = models.IntegerField(default=0)
    accuracy = models.CharField(max_length=32)

    def __str__(self):
        return f"Done by: {self.user}"


class CustomText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="texts")
    text = models.TextField()

    def __str__(self):
        return f"Written by: {self.user}"