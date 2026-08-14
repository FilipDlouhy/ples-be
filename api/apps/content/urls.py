from rest_framework.routers import SimpleRouter

from .controllers.landing import LandingController

router = SimpleRouter(trailing_slash=False)
router.register("pages/landing", LandingController, basename="landing")

urlpatterns = router.urls
