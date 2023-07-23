from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    This is the User model which inherits from the AbstractUser model.

    The AbstractUser model is a built-in Django model that provides the
    essential fields and behaviors for the user model.

    The User model has the following fields:
    - username: a CharField that is the username of the user
    - password: a CharField that is the password of the user
    - email: a CharField that is the email of the user
    - followers: a ManyToManyField that is the followers of the user
    - following: a ManyToManyField that is the following of the user
    """

    followers = models.ManyToManyField(
        "self", blank=True, related_name="following", symmetrical=False
    )  # this is a ManyToManyField that is the followers of the user and it is a self-referential field
    # the related_name attribute is the name of the reverse relation from the User model back to itself
    # the symmetrical attribute is set to False because when a user follows another user, the other user does not automatically follow the user back (i.e. the relationship is not symmetrical)

    def __str__(self):
        return f"{self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()],
        }

    # Returns the number of following of the user
    def following_count(self):
        return self.following.count()

    # Returns the number of followers of the user
    def followers_count(self):
        return self.followers.count()

    # Returns the number of posts of the user
    def posts_count(self):
        return self.posts.count()

    # Returns the posts of following of the user
    def following_posts(self):
        return self.following.all().values_list("posts", flat=True)


class Post(models.Model):
    """
    This is the Post model.

    The Post model has the following fields:
    - user: a ForeignKey that is the user who created the post
    - text: a TextField that is the text of the post
    - timestamp: a DateTimeField that is the timestamp of the post
    - likes: a ManyToManyField that is the users who liked the post

    The Post model has the following methods:
    - serialize: returns the post in a dictionary format
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )  # this is a ForeignKey that is the user who created the post
    text = models.TextField(
        max_length=1000
    )  # this is a TextField that is the text of the post
    timestamp = models.DateTimeField(
        auto_now_add=True
    )  # this is a DateTimeField that is the timestamp of the post
    likes = models.ManyToManyField(
        User, related_name="liked_posts"
    )  # this is a ManyToManyField that is the users who liked the post and it is a self-referential field

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
        """
        This is the Meta class of the Post model.

        The Meta class specifies the ordering of the posts in the database.
        """

        ordering = ["-timestamp"]
