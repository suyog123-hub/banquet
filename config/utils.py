import uuid
import base64
import secrets
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    digits = "0123456789abcdef"
    return ''.join(secrets.choice(digits) for _ in range(6))

def store_otp(user_id, otp, purpose):
    cache_key = f"otp:{user_id}"
    cache.set(cache_key, {"otp": otp, "purpose": purpose}, timeout=600)

    
def send_otp_email(email, otp):
    send_mail(
        subject="Your verification code",
        message=f"Your OTP code is {otp}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )

def verify_otp(user_id, otp, expected_purpose):
    cache_key = f"otp:{user_id}"
    stored_data = cache.get(cache_key)

    if stored_data is None:
        return False, "OTP expired or not found"

    if stored_data.get("otp") != otp:
        return False, "Invalid OTP"

    if stored_data.get("purpose") != expected_purpose:
        return False, "OTP purpose mismatch"

    cache.delete(cache_key)
    return True, None

def generate_reset_token(email):
    # Combine email + UUID
    raw = f"{email}:{uuid.uuid4()}"
    # Encode to make it URL-safe
    return base64.urlsafe_b64encode(raw.encode()).decode()

def decode_reset_token(token):
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        email, uid = raw.split(":")
        return email, uid
    except Exception:
        return None, None
