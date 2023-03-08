from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)



class Post(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    people_like = models.ManyToManyField(User, related_name="liked_posts", null=True, blank=True)

    def __str__(self):
        return f"Posted by: {self.user}"

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "user_id": self.user.id,
        }