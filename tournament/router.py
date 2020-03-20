from rest_framework import routers
from .views import PlayerViewSet, TeamViewSet, CoachViewSet, GameViewset, LoginTrackerViewSet

router = routers.DefaultRouter()
router.register('player', PlayerViewSet)
router.register('team', TeamViewSet)
router.register('coach', CoachViewSet)
router.register('game', GameViewset)
router.register('loginTracker', LoginTrackerViewSet)