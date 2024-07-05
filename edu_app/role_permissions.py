from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superuser'

class IsSuperuserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'superuser' or request.user.role == 'branch_admin')

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'
    
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
