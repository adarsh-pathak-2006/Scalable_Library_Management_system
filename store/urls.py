from django.urls import path
from .views import CategoryAPI, CategoryDetailAPI, BookAPI, BookDetailAPI

urlpatterns = [
    path('category/', CategoryAPI.as_view()),
    path('category/<int:pk>/', CategoryDetailAPI.as_view()),
    path('book/', BookAPI.as_view()),
    path('book/<int:pk>/', BookDetailAPI.as_view())
]
