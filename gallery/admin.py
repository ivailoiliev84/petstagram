from django.contrib import admin
from gallery.models import Post, PostComment

# Register your models here.


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'image', 'created_at', 'updated_at']


@admin.register(PostComment)
class AdminPostComment(admin.ModelAdmin):
    list_display = ['text', 'user', 'post', 'created_at']