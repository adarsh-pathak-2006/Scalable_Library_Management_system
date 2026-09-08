from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile
from lend.models import Cart

User=get_user_model()

@receiver(post_save, sender=User)
def CreateProfileSignal(sender, instance, created, **kwargs):
    if created:
        profile_data=Profile.objects.create(user=instance)
        Cart.objects.create(user=profile_data)
        