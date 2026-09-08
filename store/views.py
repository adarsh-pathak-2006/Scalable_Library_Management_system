from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Category, Book
from rest_framework.response import Response
from config.pagination import GeneralPagination
from .serializers import CategorySerializer, BookGetSerializer, BookWriteSerializer
from django.core.cache import cache
from config.cache_keys import category_cache_key, books_cache_key

class CategoryAPI(APIView):
    def get(self, request):
        page_no=request.query_params.get("page", "1")
        cached_data=cache.get(category_cache_key(page_no))
        if cached_data:
            return Response(cached_data, status=200)
        paginator=GeneralPagination()
        data=paginator.paginate_queryset(Category.objects.all(), request, view=self)
        serial=CategorySerializer(data, many=True)
        response=paginator.get_paginated_response(serial.data)
        cache.set(category_cache_key(page_no), response.data, timeout=300)
        return response

    def post(self, request):
        serial=CategorySerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

class CategoryDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

class BookAPI(APIView):
    def get(self, request):
        page_no=request.query_params.get("page", "1")
        cached_data=cache.get(books_cache_key(page_no))
        if cached_data:
            return Response(cached_data, status=200)
        paginator=GeneralPagination()
        data=paginator.paginate_queryset(Book.objects.select_related('category').filter(is_avaliable=True), request, view=self)
        serial=BookGetSerializer(data, many=True)
        response=paginator.get_paginated_response(serial.data)
        cache.set(books_cache_key(page_no), response.data, timeout=300)
        return response

    def post(self, request):
        serial=BookWriteSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

class BookDetailAPI(RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method=='GET':
            return [BookGetSerializer]
        return [BookWriteSerializer]
    queryset=Book.objects.select_related('category').all()