from django.urls import path

from . import views

urlpatterns = [
    path(
        "", views.index, name="index"
    ),  # this is the home page where all the posts are displayed in reverse chronological order and where the user can create a new post
    path("login", views.login_view, name="login"),  # this is the login page
    path(
        "logout", views.logout_view, name="logout"
    ),  # this is the logout page
    path(
        "register", views.register, name="register"
    ),  # this is the register page
    path(
        "network/posts", views.posts, name="posts"
    ),  # this is API route that returns all posts in reverse chronological order
    path(
        "network/posts/<int:post_id>", views.post, name="post"
    ),  # this is API route which allows the user to edit
    path(
        "profile/<str:user_id>", views.profile, name="profile"
    ),  # this is the profile page
    path(
        "network/like/<int:post_id>", views.like, name="like"
    ),  # this is the API route that allows the user to like a post and unlike a post
    path(
        "network/follow/<str:user_id>", views.follow, name="follow"
    ),  # this is the API route that allows the user to follow a user and unfollow a user
    path(
        "following", views.following, name="following"
    ),  # this is the following page
]
