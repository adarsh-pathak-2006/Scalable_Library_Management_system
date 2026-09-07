from django.shortcuts import get_object_or_404
from .models import Profile, College
from rest_framework.views import APIView
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, OtpSerializer, PasswordSerializer
from django.db.models import Q
from rest_framework.response import Response
import random
from .cache_keys import cached_session_key

User=get_user_model()

class RegisterAPI(APIView):
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            mobile_no=serial.validated_data['mobile_no']
            role=serial.validated_data['role']
            college=serial.validated_data['college']

            if User.objects.filter(Q(username=username), Q(email=email), Q(mobile_no=mobile_no)).exists():
                return Response({'message':'username or email or mobile_no already exists'}, status=400)
            user_code=random.randint(10000000, 99999999)
            key=cached_session_key(user_code)
            cache.set(key, {'username':username, 'email':email, 'mobile_no':mobile_no, 'role':role, 'college':college}, timeout=500)
            return Response({'message':'otp sent on the mobile no', 'session_code':user_code})


