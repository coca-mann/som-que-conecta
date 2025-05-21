from rest_framework.permissions import BasePermission


class IsTutorOrOng(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        try:
            user_type = user.userprofile.user_type
            return user_type in [2, 3]
        except AttributeError:
            return False
