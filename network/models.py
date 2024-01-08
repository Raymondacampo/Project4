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
    
    # def serialize(self):
    #     return {
    #         "id":self.id,
    #         "creator":self.creator,
    #         "content":self.content,
    #         "created": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
    #         "likes": self.likes
    #     }
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="info")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")

    def __str__(self):
        return f"{self.user}"
    
    def serialize(self):
        return {
            "id":self.id,
            "user":self.user,
            "following": [user for user in self.following.all()],
            "followers": [user for user in self.followers.all()]
        }