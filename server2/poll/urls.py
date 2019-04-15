from .views import PollViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.trailing_slash = '/?'
router.register(r'poll', PollViewSet, base_name='v1_poll')

api_urlpatterns = router.urls