from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
# Create your models here.

UserModel = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    image = CloudinaryField()

    title = models.CharField (max_length=50)
    description = models.TextField(max_length=200)
