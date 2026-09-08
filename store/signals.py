from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Category, Book
from config.cache_keys import category_cache_key, books_cache_key
from django.core.cache import cache

@receiver(post_save, sender=Category)
def cache_invalidation_signal_for_category(sender, instance, created, **kwargs):
    for i in range(1, 101):
        cache.delete(category_cache_key(page_no=i))    

@receiver(post_save, sender=Book)
def cache_invalidation_signal_for_book(sender, instance, created, **kwargs):
    for i in range(1, 101):
        cache.delete(books_cache_key(page_no=i))