from rest_framework import routers

from .views import TypeConfViewSet, ConferenceViewSet, ConferenceUserViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register('typeconference', TypeConfViewSet)
router.register('conference', ConferenceViewSet)
router.register('conferenceuser', ConferenceUserViewSet)

urlpatterns = router.urls
