from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CartBook, Issue, IssuedBook, Cart
from store.models import Book
from config.cache_keys import cart_books_cache_key, issued_books_key
from django.core.cache import cache

@receiver(post_save, sender=CartBook)
def cache_invalidation_signal(sender, instance, created, **kwargs):
    cache.delete(cart_books_cache_key(user_id=instance.cart.user.user.id))

@receiver(post_save, sender=IssuedBook)
def adding_books_in_IssueBook_signal(sender, instance, created, **kwargs):
    cache.delete(issued_books_key(user_id=instance.issue.cart.user.user.id))

@receiver(post_save, sender=Issue)
def reducing_the_avaliablequantity_after_ordering(sender, instance, created, **kwargs):
    cartbook_data=CartBook.objects.select_related('cart').filter(cart=instance.cart)
    for item in cartbook_data:
        item.book.quantity = item.book.quantity - item.quantity
        item.book.save()

