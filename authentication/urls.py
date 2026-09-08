from django.urls import path
from .views import CustomRefreshTokenAPI, CustomTokenObtainAPI, RegisterAPI, OtpVerificationAPI, SetPasswordAPI, MyProfileAPI, CollegeAPI

urlpatterns = [
    path('api/token/', CustomTokenObtainAPI.as_view()),
    path('api/token/refresh/', CustomRefreshTokenAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('otp-verify/<int:code>/', OtpVerificationAPI.as_view()),
    path('password-setup/<int:code>/', SetPasswordAPI.as_view()),
    path('my-profile/', MyProfileAPI.as_view()),
    path('colleges/', CollegeAPI.as_view())
]
