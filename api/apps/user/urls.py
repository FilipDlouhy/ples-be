from rest_framework.routers import SimpleRouter

from .controllers.auth import AuthController

router = SimpleRouter(trailing_slash=False)
router.register("", AuthController, basename="auth")

urlpatterns = router.urls
