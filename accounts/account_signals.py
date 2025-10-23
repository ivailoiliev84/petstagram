from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

UserModel = get_user_model()

@receiver(signal=post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
