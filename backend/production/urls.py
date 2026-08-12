from rest_framework.routers import DefaultRouter
from .views import BOMHeaderViewSet, BOMLineViewSet, WorkOrderViewSet, MaterialReservationViewSet, MaterialIssueViewSet, FGReceiptViewSet

router = DefaultRouter()
router.register('bom-headers', BOMHeaderViewSet)
router.register('bom-lines', BOMLineViewSet)
router.register('work-orders', WorkOrderViewSet)
router.register('reservations', MaterialReservationViewSet)
router.register('issues', MaterialIssueViewSet)
router.register('fg-receipts', FGReceiptViewSet)

urlpatterns = router.urls