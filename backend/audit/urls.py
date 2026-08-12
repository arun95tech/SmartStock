from rest_framework.routers import DefaultRouter
from .views import AuditTrailViewSet

router = DefaultRouter()
router.register('entries', AuditTrailViewSet)

urlpatterns = router.urls