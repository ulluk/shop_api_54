from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
    
class IsAnonymous(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
    
class CanEditWithin15Minutes(BasePermission):
    def has_object_permission(self, request, view, obj):
        time_passed = timezone.now() - obj.created_at
        print("time", time_passed)
        return time_passed <= timedelta(minutes=15)
    

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        
        if not request.user.is_staff:
            return False
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method == "POST":
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        return True