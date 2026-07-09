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
<<<<<<< HEAD
            

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

class AdminStaffAll_UserGet(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in ["POST","PUT","DELETE"]:
            if user.is_superuser or user.is_staff:
                return True
            return False
        if request.method == "GET":
            return True
=======
>>>>>>> 371819d (file updated)

class RoleBasedUserPermission(BasePermission):
    """
    Superadmin → full CRUD
    Staff → create, read, update (but not delete)
    Normal user → CRUD only on their own profile
    """

    def has_permission(self, request, view):
        role = request.user.role

        # Superadmin → allow everything
        if role == "superadmin":
            return True

        # Staff → allow create, read, update
        elif role == "staff":
            return request.method in ["GET", "POST", "PUT", "PATCH"]

        # Normal user → allow CRUD but only on their own profile (checked below)
        elif role == "user":
            return request.method in ["GET", "PUT", "PATCH", "DELETE"]

        return False

    def has_object_permission(self, request, view, obj):
        role = request.user.role

        # Superadmin → full access
        if role == "admin":
            return True

        # Staff → can only manage users in their own organization
        elif role == "staff":
            return obj.organization == request.user.organization

        # Normal user → can only CRUD their own profile
        elif role == "user":
            return obj == request.user

        return False
