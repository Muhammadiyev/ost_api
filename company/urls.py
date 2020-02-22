from rest_framework import routers

from .views import (
    RoleViewSet, 
    RoleOfUserViewSet, 
    DepartmentViewSet,
    DepartmentOfUserViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register('role', RoleViewSet)
router.register('roleofusers', RoleOfUserViewSet)
router.register('department', DepartmentViewSet)
router.register('departmentofuser', DepartmentOfUserViewSet)
urlpatterns = router.urls
