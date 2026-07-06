from rest_framework.throttling import UserRateThrottle

class OTPResendThrottle(UserRateThrottle):
    scope = "otp_resend"
    rate = '3/hr'
