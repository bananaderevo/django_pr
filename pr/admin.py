from django.contrib import admin

from .models import Comments, Post, User


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'display_comments', 'is_published']


@admin.register(Comments)
class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ['is_published', 'name', 'author', 'id']