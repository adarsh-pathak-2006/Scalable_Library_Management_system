from django.core.cache import cache

def cached_session_key(code):
    return f"cached_session_key_user_code:{code}"

def cached_otp_key(user_code):
    return f"otp_sent_on_mobileno_with_sessioncode:{user_code}"

def profile_cache_key(pk):
    return f"cached_profile_page_userID:{pk}"

# --- Version-based cache keys for paginated lists ---
# The version is stored as a separate key. Bumping it (in signals.py)
# automatically makes all old page-based cache keys stale, with a single
# Redis operation instead of 100 deletes.

def category_cache_version_key():
    return "category_cache_version"

def books_cache_version_key():
    return "books_cache_version"

def category_cache_key(page_no):
    version = cache.get(category_cache_version_key()) or 0
    return f"cached_category_page:{page_no}:v{version}"

def books_cache_key(page_no):
    version = cache.get(books_cache_version_key()) or 0
    return f"cached_books_page:{page_no}:v{version}"

def cart_books_cache_key(user_id):
    return f"books_in_cart_key_user:{user_id}"

def issued_books_key(user_id):
    return f"Issued_books_keys_userid:{user_id}"