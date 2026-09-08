from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CartBook
from config.cache_keys import cart_books_cache_key
from django.core.cache import cache

@receiver(post_save, sender=CartBook)
def cache_invalidation_signal(sender, instance, created, **kwargs):
    cache.delete(cart_books_cache_key(user_id=instance.cart.user.user.id))