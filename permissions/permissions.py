from rest_framework import permissions

from users.models import CustomUser
from conference.models import Conference


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        return False


class UserHasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        user = CustomUser.objects.get(pk=view.kwargs['pk'])
        if request.user == user:
            return True
        more_condition = True
        if more_condition:
            return False
        return False


class IsAdminOrConferenceOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True
        conference = Conference.objects.get(id=obj.id)
        user = CustomUser.objects.filter(conference_of_user=conference)

        if request.user in user:
            return True
        return False


class IsAdminOrDriverOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        order = Order.objects.get(id=obj.id)
        if request.user.user_type == 'DRIVER':
            if order.driver.id == request.user.id:
                return True
        return False


class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        return False


class IsAdminOrIsSameUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif obj.id == request.user.id:
            return True
        return False
