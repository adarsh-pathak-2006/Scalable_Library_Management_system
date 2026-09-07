from django.shortcuts import get_object_or_404
from .models import Profile, College
from rest_framework.views import APIView
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, OtpSerializer, PasswordSerializer, ProfileSerializer
from django.db.models import Q
from rest_framework.response import Response
import random
from .cache_keys import cached_session_key, cached_otp_key, profile_cache_key
from .tasks import OtpGenerationTask

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
            cache.set(key, {'username':username, 'email':email, 'mobile_no':mobile_no, 'role':role, 'college':college}, timeout=300)
            OtpGenerationTask.delay(user_code)
            return Response({'message':'otp sent on the mobile no', 'session_code':user_code})
        return Response(serial.errors, status=400)


class OtpVerificationAPI(APIView):
    def post(self, request, code):
        serial=OtpSerializer(data=request.data)
        if serial.is_valid():
            otp=serial.validated_data['otp']
            session=cache.get(cached_session_key(code=code))
            generated_otp=cache.get(cached_otp_key(user_code=code))
            if generated_otp==otp:
                session['is_verified']=True
                cache.set(cached_session_key(code=code), session, timeout=300)
                return Response({'message':'otp verified set the password now'}, status=200)
            return Response({'message':'otp not correct_try again'}, status=400)
        return Response(serial.errors, status=400)

class SetPasswordAPI(APIView):
    def post(self, request, code):
        serial=PasswordSerializer(data=request.data)
        if serial.is_valid():
            password=serial.validated_data['password']
            cached_session=cache.get(cached_session_key(code=code))
            if cached_session['is_verified']==True:
                User.objects.create_user(username=cached_session['username'], email=cached_session['email'], password=password, mobile_no=cached_session['mobile_no'], role=cached_session.get('role'), college=cached_session['college'])
                return Response({'message':'User registration Successfull'}, status=201)
            return Response({'message':'not verified'}, status=400)
        return Response(serial.errors, status=400)

class MyProfileAPI(APIView):
    def get(self, request):
        cached_data=cache.get(profile_cache_key(request.user.id))
        if cached_data:
            return Response(cached_data, status=200)
        data=get_object_or_404(User.objects.select_related('user'), user=request.user)
        serial=ProfileSerializer(data)
        return Response(serial.data, status=200)

    def patch(self, request):
        instance=get_object_or_404(Profile.objects.select_related('user'), user=request.user)
        serial=ProfileSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)