from rest_framework import routers

from .views import (
    DepartmentViewSet,
    DepartmentOfUserViewSet,
    DepartmentOfUsersViewSet,
    CompanyViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register('company', CompanyViewSet)
router.register('department', DepartmentViewSet)
router.register('departmentofuser', DepartmentOfUserViewSet)
router.register('departmentofusers', DepartmentOfUsersViewSet)
urlpatterns = router.urls
