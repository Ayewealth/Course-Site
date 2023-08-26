from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
        # return request.user.groups.filter(name='Student').exists()

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
        # return request.user.groups.filter(name='Instructor').exists()
    
    # def has_permission(self, request, view):
    #     if request.user.groups.filter(name='Instructor').exists():
    #         return super().has_permission(request, view)