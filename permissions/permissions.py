from rest_framework import permissions

from users.models import CustomUser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        return False


class UserHasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.role.id == request.user.id

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_staff:
    #         return True
    #     user = CustomUser.objects.get(pk=view.kwargs['pk'])
    #     if request.user == user:
    #         return True
    #        # if have more condition then apply
    #     more_condition = 'У вас нет прав для выполнения этой операции.'
    #     if more_condition:
    #         return False
    #     return False


class IsAdminOrCourierOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        parent = Parcel.objects.get(id=obj.id)
        order = CustomUser.objects.get(parent=parent)
        if request.user.user_type == 'COURIER':
            if order.courier.id == request.user.id:
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
