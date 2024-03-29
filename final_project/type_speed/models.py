from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    gender = models.CharField(max_length=32, default='other')


class CustomText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="texts")
    title = models.CharField(max_length=64, default="Blank")
    text = models.TextField()

    def __str__(self):
        return f"Written by: {self.user}"
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "user": self.user.username
        }
    

class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores")
    words_min = models.IntegerField(default=0)
    chars_min = models.IntegerField(default=0)
    accuracy = models.CharField(max_length=32)
    custom = models.BooleanField(default=False) 
    text = models.ForeignKey(CustomText, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Done by: {self.user}"


