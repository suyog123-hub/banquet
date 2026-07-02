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
