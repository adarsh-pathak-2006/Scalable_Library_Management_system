from rest_framework import serializers
from .models import Profile, College
from django.contrib.auth import get_user_model

User=get_user_model()

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    college=serializers.PrimaryKeyRelatedField(queryset=College.objects.all())
    class Meta:
        model=User
        fields=['username', 'email', 'mobile_no', 'role', 'college']

class OtpSerializer(serializers.Serializer):
    otp=serializers.CharField()

class PasswordSerializer(serializers.Serializer):
    password=serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Profile
        fields='__all__'