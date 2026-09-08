from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import Cart, Issue, CartBook, IssuedBook

@shared_task
def adding_data_in_the_issuebookmodel_task(cart_id, issue_id):
    cart_data=get_object_or_404(Cart, id=cart_id)
    issue_data=get_object_or_404(Issue, id=issue_id)
    cartbook_data=CartBook.objects.select_related('cart').filter(cart=cart_data)
    for data in cartbook_data:
        IssuedBook.objects.create(issue=issue_data, book=data.book, quantity=data.quantity)

