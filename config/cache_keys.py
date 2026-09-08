def cached_session_key(code):
    return f"cached_session_key_user_code:{code}"

def cached_otp_key(user_code):
    return f"otp_sent_on_mobileno_with_sessioncode:{user_code}"

def profile_cache_key(pk):
    return f"cached_profile_page_userID:{pk}"

def category_cache_key(page_no):
    return f"cached_category_page:{page_no}"

def books_cache_key(page_no):
    return f"cached_books_page:{page_no}"