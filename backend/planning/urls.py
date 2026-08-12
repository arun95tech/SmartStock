from rest_framework.routers import DefaultRouter
from .views import ForecastRunViewSet, ReorderRecommendationViewSet, ABCClassificationRunViewSet, SupplierKPIViewSet, SupplierRiskScoreViewSet

router = DefaultRouter()
router.register('forecasts', ForecastRunViewSet)
router.register('recommendations', ReorderRecommendationViewSet)
router.register('abc-runs', ABCClassificationRunViewSet)
router.register('supplier-kpis', SupplierKPIViewSet)
router.register('supplier-risk', SupplierRiskScoreViewSet)

urlpatterns = router.urls