from django.urls import path
from .views import CartAPI, AddToCartAPI, IssuedBooksViewAPI, BooksIssueAPI

urlpatterns = [
    path('cart/', CartAPI.as_view()),
    path('addtocart/<int:pk>/', AddToCartAPI.as_view()),
    path('issue/<int:pk>/', BooksIssueAPI.as_view()),
    path('issued-books/', IssuedBooksViewAPI.as_view())
]
