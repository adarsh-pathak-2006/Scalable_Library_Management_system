from celery import shared_task
from django.core.cache import cache
import random

@shared_task
def OtpGenerationTask(user_code):
    cached_session=cache.get(user_code)
    mobile_no=cached_session['mobile_no']
    generated_otp=random.randint(100000, 999999)
    return f"mobile_no:{mobile_no}..otp:{generated_otp}"
