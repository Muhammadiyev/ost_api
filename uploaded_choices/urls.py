from rest_framework import routers

from .views import (
    UploadedFileViewSet
)

router = routers.DefaultRouter(trailing_slash=False)

router.register('uploadfile', UploadedFileViewSet)

urlpatterns = router.urls
