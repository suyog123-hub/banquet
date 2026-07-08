from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class OTPResendThrottle(UserRateThrottle):
    scope = "otp_resend"
    rate = "3/hr"   # 3 requests per hour per user

class RegisterViewThrottle(AnonRateThrottle):
    scope = "register"
    rate = "5/day"  # 5 requests per day per anonymous IP

class LoginViewThrottle(AnonRateThrottle):
    scope = "login"
    rate = "10/day" # 10 login attempts per day per anonymous IP

class ChangePasswordThrottle(UserRateThrottle):
    scope = "change_password"
    rate = "3/90d"  # 3 password changes per 90 days per user
