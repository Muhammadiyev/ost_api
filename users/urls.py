from rest_framework import routers

from .views import (
    UserViewSet, 
    AuthViewSet, 
    UserOfRoleSerializerViewSet, 
    UserOfDepartmentViewSet,
    UserOfParentSerializerViewSet
)



router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('userofdepartment', UserOfDepartmentViewSet, basename='auth')
router.register('userofrole', UserOfRoleSerializerViewSet, basename='auth')
router.register('userofparent', UserOfParentSerializerViewSet, basename='auth')

router.register('users', UserViewSet)

urlpatterns = router.urls