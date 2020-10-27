from rest_framework.permissions import BasePermission

class MyPermission1(BasePermission):
    def has_permission(self,request,view):
        if request.user['userrole']=="1":
            return True
        return False
