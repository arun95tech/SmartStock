from rest_framework.routers import DefaultRouter
from .views import StockLocationViewSet, StockLedgerViewSet, StockAdjustmentViewSet

router = DefaultRouter()
router.register('locations', StockLocationViewSet)
router.register('ledger', StockLedgerViewSet)
router.register('adjustments', StockAdjustmentViewSet)

urlpatterns = router.urls