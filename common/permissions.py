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
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.method != "POST"
        )
    
    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.method in SAFE_METHODS + ("PUT", "PATCH", "DELETE")
        )