from rest_framework import routers

from .views import UserViewSet, AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
# router.register('api', AuthViewSetCompany, basename='auth')
router.register('users', UserViewSet)

urlpatterns = router.urls