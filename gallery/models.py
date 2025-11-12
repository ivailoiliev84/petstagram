from django.db import models
from django.contrib.auth import get_user_model
# from cloudinary.models import CloudinaryField
# Create your models here.

UserModel = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='post/', blank=True, null=True)

    title = models.CharField (max_length=30)
    description = models.TextField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class PostLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class PostDislike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post_dislikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
   