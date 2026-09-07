def cached_session_key(code):
    return f"cached_session_key_user_code:{code}"

def cached_otp(mobile_no, user_code):
    return f"otp_sent_on_mobileno:{mobile_no}_with_sessioncode:{user_code}"