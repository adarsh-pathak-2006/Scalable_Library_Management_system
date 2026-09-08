from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartBookSerializer, IssuedBookSerializer
from .models import Issue, CartBook, Cart, IssuedBook
from store.models import Book
from config.cache_keys import cart_books_cache_key, issued_books_key
from django.core.cache import cache
from .tasks import adding_data_in_the_issuebookmodel_task
from config.permissions import IsStudent
from config.throttling import GeneralThrottling

class CartAPI(APIView):
    permission_classes=[IsStudent]
    throttle_classes=[GeneralThrottling]
    def get(self, request):
        cached_data=cache.get(cart_books_cache_key(user_id=request.user.id))
        if cached_data:
            return Response(cached_data, status=200)
        cart_data=get_object_or_404(Cart.objects.select_related('user__user'), user__user=request.user)
        data=CartBook.objects.select_related('cart', 'book').filter(cart=cart_data)
        serial=CartBookSerializer(data, many=True)
        cache.set(cart_books_cache_key(user_id=request.user.id), serial.data, timeout=300)
        return Response(serial.data, status=200)

class AddToCartAPI(APIView):
    permission_classes=[IsStudent]
    throttle_classes=[GeneralThrottling]
    def post(self, request, pk):
        serial=CartBookSerializer(data=request.data)
        if serial.is_valid():
            cart_data=get_object_or_404(Cart.objects.select_related('user__user'), user__user=request.user)
            book_data=get_object_or_404(Book, id=pk)
            if CartBook.objects.filter(cart=cart_data, book=book_data).exists():
                cart_book=CartBook.objects.select_related('cart__user__user', 'book').get(cart=cart_data, book=book_data)
                cart_book.quantity=cart_book.quantity + 1
                cart_book.save()
                return Response(CartBookSerializer(cart_book).data, status=200)
            else:
                serial.save(cart=cart_data, book=book_data)
                return Response(serial.data, status=201)
        else:
            return Response(serial.errors, status=400)

class BooksIssueAPI(APIView):
    permission_classes=[IsStudent]
    throttle_classes=[GeneralThrottling]
    def post(self, request, pk):
        # Enforce ownership: only the cart's owner can issue it.
        # Previously, any student could pass any cart's pk and issue someone else's books.
        cart_data=get_object_or_404(
            Cart.objects.select_related('user__user'),
            id=pk,
            user__user=request.user  # ownership check
        )
        # Ensure the cart actually has books before creating an Issue record
        if not CartBook.objects.filter(cart=cart_data).exists():
            return Response({'message': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        issue_data=Issue.objects.create(cart=cart_data)
        adding_data_in_the_issuebookmodel_task.delay(cart_id=pk, issue_id=issue_data.id)
        return Response({'message':'Books issued successfully.'}, status=201)

class IssuedBooksViewAPI(APIView):
    permission_classes=[IsStudent]
    throttle_classes=[GeneralThrottling]
    def get(self, request):
        cached_data=cache.get(issued_books_key(user_id=request.user.id))
        if cached_data:
            return Response(cached_data, status=200)
        # Use .filter() instead of get_object_or_404 — a student can have
        # multiple issued book records, and get_object_or_404 crashes with
        # MultipleObjectsReturned in that case.
        data=IssuedBook.objects.select_related(
            'issue__cart__user__user', 'book'
        ).filter(issue__cart__user__user=request.user)
        serial=IssuedBookSerializer(data, many=True)
        cache.set(issued_books_key(user_id=request.user.id), serial.data, timeout=300)
        return Response(serial.data, status=200)
