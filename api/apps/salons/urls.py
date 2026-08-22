from rest_framework.routers import SimpleRouter

from .controllers.makers import MakerController

router = SimpleRouter(trailing_slash=False)
router.register("makers", MakerController, basename="maker")

urlpatterns = router.urls
