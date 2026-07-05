# permissions.py
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from config.response import server_error_response


class AdminGetOrPostAll(BasePermission):
    """
    Custom permission:
    - GET, DELETE: Only admin users (is_staff or is_superuser)
    - POST: Anyone can create (no authentication required)
    """
    def has_permission(self, request, view):
            try:
                user = request.user
                # GET, DELETE - Only admin
                if request.method in ['GET', 'DELETE']:
                    if user.is_superuser or user.is_staff:
                        return True
                # POST - Allow anyone (including anonymous)
                if request.method == 'POST':
                    return True
                return False
            
            except Exception as e :
                 return Response ({
                      'message' : str(e)
                 },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class SuperAdminAll_StaffGetPost_userPost(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        
        if user.is_staff:
            return request.method in ['GET', 'POST']
        
        if user.is_authenticated:
            return request.method == 'POST'
        

        return False