import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post

MAX_POST_LENGTH = 280
POST_PER_PAGE = 10

login_url = "/login"


def index(request):
    """
    This view is used to render the index page.

    Parameters:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The response object.
    """
    posts = Post.objects.all().order_by("-timestamp").all()
    paginator = Paginator(posts, POST_PER_PAGE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/index.html",
        {"page_obj": page_obj, "posts": page_obj.object_list},
    )


def login_view(request):
    """
    This view is used to render the login page.

    Parameters:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    """
    This view is used to logout the user.

    Parameters:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The response object.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    This view is used to render the register page.

    Parameters:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "network/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "network/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required(login_url=login_url)
def posts(request):
    """
    This view is used to create a new post.

    Parameters:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        user = request.user
        if len(text) > MAX_POST_LENGTH:
            return JsonResponse(
                {"error": "Post must be 280 characters or less."}, status=400
            )
        new_post = Post(user=user, text=text)
        new_post.save()
        return JsonResponse(
            {"message": "Post created successfully."}, status=201
        )


@csrf_exempt
@login_required(login_url=login_url)
def post(request, post_id):
    """
    This view is used to edit a post.

    Parameters:
        request (HttpRequest): The request object used to generate this response.
        post_id (int): The id of the post to edit.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == "PUT":
        data = json.loads(request.body)
        text = data.get("text", "")
        post = Post.objects.get(pk=post_id)
        if post.user != request.user:
            return JsonResponse(
                {"error": "You are not allowed to edit this post."},
                status=403,
            )
        if len(text) > MAX_POST_LENGTH:
            return JsonResponse(
                {"error": "Post must be 280 characters or less."}, status=400
            )
        post.text = text
        post.save()
        return JsonResponse(
            {"message": "Post updated successfully."}, status=201
        )


def profile(request, user_id):
    """
    This view is used to render the profile page.

    Parameters:
        request (HttpRequest): The request object used to generate this response.
        user_id (int): The id of the user.

    Returns:
        HttpResponse: The response object.
    """
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user)
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, POST_PER_PAGE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/profile.html",
        {
            "page_obj": page_obj,
            "posts": page_obj.object_list,
            "profile": user,
        },
    )


@csrf_exempt
@login_required(login_url=login_url)
def like(request, post_id):
    """
    This view is used to like a post.

    Parameters:
        request (HttpRequest): The request object used to generate this response.
        post_id (int): The id of the post to like.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            post.save()
            return JsonResponse(
                {
                    "message": "Post unliked successfully.",
                    "likes": post.likes.count(),
                    "liked": False,
                },
                status=201,
            )
        else:
            post.likes.add(user)
            post.save()
            return JsonResponse(
                {
                    "message": "Post liked successfully.",
                    "likes": post.likes.count(),
                    "liked": True,
                },
                status=201,
            )


@csrf_exempt
@login_required(login_url=login_url)
def follow(request, user_id):
    """
    This view is used to follow a user.

    Parameters:
        request (HttpRequest): The request object used to generate this response.
        user_id (int): The id of the user to follow.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == "PUT":
        user = request.user
        following = User.objects.get(pk=user_id)
        if user == following:
            return JsonResponse(
                {"error": "You are not allowed to follow yourself."},
                status=403,
            )
        if user in following.followers.all():
            following.followers.remove(user)
            following.save()
            return JsonResponse(
                {
                    "message": "User unfollowed successfully.",
                    "followers": following.followers.count(),
                    "followed": False,
                },
                status=201,
            )
        else:
            following.followers.add(user)
            following.save()
            return JsonResponse(
                {
                    "message": "User followed successfully.",
                    "followers": following.followers.count(),
                    "followed": True,
                },
                status=201,
            )


@login_required(login_url=login_url)
def following(request):
    """
    This view is used to render the following page.

    Parameters:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The response object.
    """
    user = request.user
    posts = Post.objects.filter(user__in=user.following.all())
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, POST_PER_PAGE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/following.html",
        {"page_obj": page_obj, "posts": page_obj.object_list},
    )
