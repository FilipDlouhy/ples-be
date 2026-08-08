from rest_framework.routers import SimpleRouter

from .controllers.site_config import SiteConfigController

router = SimpleRouter(trailing_slash=False)
router.register("config", SiteConfigController, basename="site-config")

urlpatterns = router.urls
