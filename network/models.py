from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.CharField(max_length=150)

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_post")
    
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="info")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")