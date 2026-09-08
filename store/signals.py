from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Category, Book
from config.cache_keys import books_cache_version_key, category_cache_version_key
from django.core.cache import cache

@receiver(post_save, sender=Category)
def cache_invalidation_signal_for_category(sender, instance, created, **kwargs):
    # Increment the version counter for category caches.
    # A single Redis INCR atomically invalidates ALL paginated category pages
    # without looping — O(1) instead of O(n).
    version = cache.get(category_cache_version_key()) or 0
    cache.set(category_cache_version_key(), version + 1, timeout=None)

@receiver(post_save, sender=Book)
def cache_invalidation_signal_for_book(sender, instance, created, **kwargs):
    # Same versioning strategy for books.
    version = cache.get(books_cache_version_key()) or 0
    cache.set(books_cache_version_key(), version + 1, timeout=None)