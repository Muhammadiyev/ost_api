from rest_framework import routers

from .views import DepartmentViewSet, DepartmentOfUserViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register('department', DepartmentViewSet)
router.register('departmentofusers', DepartmentOfUserViewSet)

urlpatterns = router.urls
