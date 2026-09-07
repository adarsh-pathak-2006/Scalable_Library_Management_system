from django.shortcuts import get_object_or_404
from .models import Profile, College
from rest_framework.views import APIView
from django.core.cache import cache
from django.contrib.auth import get_user_model


User=get_user_model()
