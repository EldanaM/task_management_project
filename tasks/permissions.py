from rest_framework.permissions import BasePermission

class TaskPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
            
        if user.role == 'client':
            return obj.created_by == user
            
        if request.method == 'DELETE':
            return user.role == 'admin'
            
        return True
