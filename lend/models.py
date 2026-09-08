from django.db import models
from store.models import Book
from authentication.models import Profile

class Cart(models.Model):
    user=models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username

class CartBook(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='books_in_cart')
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    added_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=models.UniqueConstraint(fields=['book', 'cart'], name='unique_book_in_cart')

    def save(self, *args, **kwargs):
        if self.quantity > self.book.quantity:
            raise "selected quantity should be lower than the avaliable stock."
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.cart.user.user.username
    
class Issue(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    issued_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart.user.user.username