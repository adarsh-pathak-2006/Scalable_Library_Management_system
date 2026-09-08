from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Category, Book

class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        read_only_fields=['created_on']

class BookGetSerializer(ModelSerializer):
    category=CategorySerializer(read_only=True)
    class Meta:
        model=Book
        fields='__all__'
        read_only_fields=['added_on', 'is_avaliable']

class BookWriteSerializer(ModelSerializer):
    category=PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model=Book
        read_only_fields=['added_on', 'is_avaliable']
