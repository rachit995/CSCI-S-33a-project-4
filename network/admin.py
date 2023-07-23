from django.contrib import admin

# Register your models here.

from .models import User, Post


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "followers",
        "following",
    )  # this is the list of followers and following of the user


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "likes",
    )  # this is the list of users who liked the post


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
