from rest_framework.permissions import BasePermission


class IsCommentAuthorOrAdmin(BasePermission):


    def has_object_permission(self, request, view, obj):
        

        if request.user == obj.user_id:
            return True
        
        if request.user.is_staff or request.user.is_superuser:
            return True