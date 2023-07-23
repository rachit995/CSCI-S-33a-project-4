from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("network/posts", views.posts, name="posts"),
    path("network/posts/<int:post_id>", views.post, name="post"),
    path("profile/<str:user_id>", views.profile, name="profile"),
    path("network/like/<int:post_id>", views.like, name="like"),
    path("network/follow/<str:user_id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
]
