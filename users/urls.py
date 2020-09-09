from rest_framework import routers
from django.urls import path, include, re_path

from .views import (
    UserAllViewSet,
    AuthViewSet,
    UserOfRoleOfDepartmentViewSet,
    UserOfDepartmentViewSet,
    UserOfRoleOfViewSet,
    UsersViewSet,
    CheckPasswordUserViewSet,
    CheckPasswordUserListViewSet,
    StatisticUsersViewSet
)


router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('userofdepartment', UserOfDepartmentViewSet, basename='auth')
router.register('userofroleofdepartment',
                UserOfRoleOfDepartmentViewSet, basename='auth')
router.register('userofrole', UserOfRoleOfViewSet, basename='auth')
router.register('users', UserAllViewSet)
router.register('usersconf', UsersViewSet)

router.register('check/password/users', CheckPasswordUserViewSet)
router.register('check/password/userslist', CheckPasswordUserListViewSet)

router.register('api/users/statistic', StatisticUsersViewSet)

urlpatterns = router.urls
