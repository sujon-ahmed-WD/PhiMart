from rest_framework import permissions  

class IsAdminOrReadOnly(permissions.BasePermission): #--------------------- Stricture 
    def has_permission(self, request, view):
        if request.method in  permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
    
# from rest_framework.permissions import BasePermission
# class IsAdminOrReadOnly(BasePermission):     -------------------- # Custom 
#     def has_permission(self, request, view):
#         if request.method =='GET':
#             return True
#         return bool(request.user and request.user.is_staff)
    

class FullDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
            
         