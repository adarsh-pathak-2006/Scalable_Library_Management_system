from celery import shared_task
from django.core.cache import cache
import random
from .cache_keys import cached_otp_key, cached_session_key
import time

@shared_task
def OtpGenerationTask(user_code):
    cached_session=cache.get(cached_session_key(user_code))
    mobile_no=cached_session['mobile_no']
    time.sleep(10)
    generated_otp=random.randint(100000, 999999)
    cache.set(cached_otp_key(mobile_no=mobile_no, user_code=user_code), generated_otp, timeout=600)
    return f"mobile_no:{mobile_no}..otp:{generated_otp}"
