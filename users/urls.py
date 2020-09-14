from rest_framework import routers
from django.urls import path, include, re_path

from .views import (
    UserAllViewSet,
    UsersListViewSet,
    AuthViewSet,
    UserOfRoleOfDepartmentViewSet,
    UserOfDepartmentViewSet,
    UserOfRoleOfViewSet,
    UsersViewSet,
    CheckPasswordUserViewSet,
    CheckPasswordUserListViewSet,
    StatisticUsersViewSet,
    StatisticUsersCityViewSet,
    StatisticUsersAllViewSet
)


router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('userofdepartment', UserOfDepartmentViewSet, basename='auth')
router.register('userofroleofdepartment',
                UserOfRoleOfDepartmentViewSet, basename='auth')
router.register('userofrole', UserOfRoleOfViewSet, basename='auth')
router.register('users', UserAllViewSet)
router.register('api/users', UsersListViewSet)
router.register('usersconf', UsersViewSet)

router.register('check/password/users', CheckPasswordUserViewSet)
router.register('check/password/userslist', CheckPasswordUserListViewSet)

router.register('api/usersstatistic', StatisticUsersViewSet)
router.register('api/citystatistic', StatisticUsersCityViewSet)
router.register('api/usersallstatistic', StatisticUsersAllViewSet)

urlpatterns = router.urls
