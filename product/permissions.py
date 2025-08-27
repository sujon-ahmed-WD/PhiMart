from rest_framework import permissions

class IsReviewAuthorOrReadonly(permissions.BasePermission): # ata holo ja sa dhakba ja ami ae page dhakta parbo ke nh 
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    
    def has_object_permission(self, request, view, obj): # amer object golo dhakbo ata 
         
        if request.method in permissions.SAFE_METHODS:
             return True
         
        if request.user.is_staff:
            return True
        
        return obj.user==request.user 
    