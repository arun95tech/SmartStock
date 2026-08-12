from rest_framework.routers import DefaultRouter
from .views import PurchaseOrderViewSet, POLineViewSet, GoodsReceiptViewSet, GRLineViewSet, QCHoldViewSet

router = DefaultRouter()
router.register('purchase-orders', PurchaseOrderViewSet)
router.register('po-lines', POLineViewSet)
router.register('goods-receipts', GoodsReceiptViewSet)
router.register('gr-lines', GRLineViewSet)
router.register('qc-holds', QCHoldViewSet)

urlpatterns = router.urls