def cached_session_key(code):
    return f"cached_session_key_user_code:{code}"

def cached_otp_key(user_code):
    return f"otp_sent_on_mobileno_with_sessioncode:{user_code}"

def profile_cache_key(pk):
    return f"cached_profile_page_userID:{pk}"