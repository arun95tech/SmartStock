from rest_framework.routers import DefaultRouter
from .views import ItemCategoryViewSet, ItemViewSet, SupplierViewSet, ItemSupplierViewSet

router = DefaultRouter()
router.register('categories', ItemCategoryViewSet)
router.register('items', ItemViewSet)
router.register('suppliers', SupplierViewSet)
router.register('item-suppliers', ItemSupplierViewSet)

urlpatterns = router.urls