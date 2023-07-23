from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", blank=True, related_name="following", symmetrical=False
    )

    def __str__(self):
        return f"{self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()],
        }

    def following_count(self):
        return self.following.count()

    def followers_count(self):
        return self.followers.count()

    def posts_count(self):
        return self.posts.count()

    def following_posts(self):
        return self.following.all().values_list("posts", flat=True)


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    text = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")

    def __str__(self):
        return f"{self.user}: {self.text}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": [user.username for user in self.likes.all()],
        }

    class Meta:
        ordering = ["-timestamp"]
