from django.contrib import admin

from .models import Comments, Post, User


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'display_comments']


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


@admin.register(Comments)
class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'id']