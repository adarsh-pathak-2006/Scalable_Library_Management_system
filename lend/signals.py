from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CartBook, Issue, IssuedBook
from config.cache_keys import cart_books_cache_key
from django.core.cache import cache

@receiver(post_save, sender=CartBook)
def cache_invalidation_signal(sender, instance, created, **kwargs):
    cache.delete(cart_books_cache_key(user_id=instance.cart.user.user.id))

# @receiver(post_save, sender=Issue)
# def adding_books_in_IssueBook_signal(sender, instance, created, **kwargs):
#     book_data=CartBook.objects.select_related('cart').filter(cart=instance)
#     for data in book_data:
#         IssuedBook.objects.create(issue=instance, book=data.book, quantity=data.quantity)
