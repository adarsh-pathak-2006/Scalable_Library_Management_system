from rest_framework.serializers import ModelSerializer
from .models import Cart, CartBook, Issue
from authentication.serializers import ProfileSerializer
from store.serializers import BookGetSerializer

class CartSerializer(ModelSerializer):
    user=ProfileSerializer(read_only=True)
    class Meta:
        model=Cart
        fields='__all__'

class CartBookSerializer(ModelSerializer):
    cart=CartSerializer(read_only=True)
    book=BookGetSerializer(read_only=True)
    class Meta:
        model=CartBook
        fields='__all__'
        read_only_fields=['added_on']

class IssueBookSerializer(ModelSerializer):
    cart=CartSerializer(read_only=True)
    class Meta:
        model=Issue
        fields='__all__'
        read_only_fields=['issued_on']
