from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartBookSerializer
from .models import Issue, CartBook, Cart
from store.models import Book
from config.cache_keys import cart_books_cache_key
from django.core.cache import cache
from .tasks import adding_data_in_the_issuebookmodel_task

class CartAPI(APIView):
    def get(self, request):
        cached_data=cache.get(cart_books_cache_key(user_id=request.user.id))
        if cached_data:
            return Response(cached_data, status=200)
        cart_data=get_object_or_404(Cart.objects.select_related('user__user'), user__user=request.user)
        data=CartBook.objects.select_related('cart').filter(cart=cart_data)
        serial=CartBookSerializer(data, many=True)
        cache.set(cart_books_cache_key(user_id=request.user.id), serial.data, timeout=300)
        return Response(serial.data, status=200)

class AddToCartAPI(APIView):
    def post(self, request, pk):
        serial=CartBookSerializer(data=request.data)
        if serial.is_valid():
            cart_data=get_object_or_404(Cart.objects.select_related('user__user'), user__user=request.user)
            book_data=get_object_or_404(Book, id=pk)
            if CartBook.objects.select_related('book').filter(book=book_data).exists():
                cart_book=CartBook.objects.select_related('cart__user__user', 'book').get(cart__user__user=request.user, book=book_data)
                cart_book.quantity=cart_book.quantity + 1
            else:
                serial.save(cart=cart_data, book=book_data)
                return Response(serial.data, status=201)
        else:
            return Response(serial.errors, status=400)

class BooksIssueAPI(APIView):
    def post(self, request, pk):
        cart_data=get_object_or_404(Cart, id=pk)
        issue_data=Issue.objects.create(cart=cart_data)
        adding_data_in_the_issuebookmodel_task.delay(cart_id=pk, issue_id=issue_data.id)
        return Response({'message':'books issued.'}, status=201)

        


