from rest_framework.throttling import UserRateThrottle

class GeneralThrottling(UserRateThrottle):
    rate="30/minute"

class TokenGenerationThrottle(UserRateThrottle):
    rate="5/minute"

class TokenRefreshThrottle(UserRateThrottle):
    rate="10/day"

class OTPVerificationThrottle(UserRateThrottle):
    rate="20/day"

class RegistrationThrottle(UserRateThrottle):
    rate="30/day"