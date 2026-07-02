from rest_framework.response import Response
from datetime import datetime

def custom_response(success: bool, message: str, data=None, status_code=200):
    """
    Global response wrapper for consistent API output.
    """
    return Response({
        "success": success,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }, status=status_code)


# --- For Success Responses ---
def success_response(message="Request successful", data=None, code=200):
    return custom_response(True, message, data, status_code=code)

def created_response(message="Resource created", data=None, code=201):
    return custom_response(True, message, data, status_code=code)


# --- For Error Responses ---
def error_response(message="Bad request", code=400):
    return custom_response(False, message, None, status_code=code)

def validation_error_response(errors, message="Validation failed", code=422):
    return custom_response(False, message, errors, status_code=code)

def unauthorized_response(message="Unauthorized", code=401):
    return custom_response(False, message, None, status_code=code)

def forbidden_response(message="Forbidden", code=403):
    return custom_response(False, message, None, status_code=code)

def not_found_response(message="Resource not found", code=404):
    return custom_response(False, message, None, status_code=code)

def conflict_response(message="Conflict", code=409):
    return custom_response(False, message, None, status_code=code)

def server_error_response(message="Internal server error", code=500):
    return custom_response(False, message, None, status_code=code)
