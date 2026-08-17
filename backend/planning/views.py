from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ForecastRun, ReorderRecommendation, ABCClassificationRun, SupplierKPI, SupplierRiskScore
from .serializers import ForecastRunSerializer, ReorderRecommendationSerializer, ABCClassificationRunSerializer, SupplierKPISerializer, SupplierRiskScoreSerializer
from .services import check_reorder
from master_data.models import Item
from inventory.models import StockLocation
from rest_framework.decorators import action
from .services import classify_items_abc


class ForecastRunViewSet(viewsets.ModelViewSet):
    queryset = ForecastRun.objects.all()
    serializer_class = ForecastRunSerializer


class ReorderRecommendationViewSet(viewsets.ModelViewSet):
    queryset = ReorderRecommendation.objects.all()
    serializer_class = ReorderRecommendationSerializer

    # Custom endpoint: POST /api/planning/recommendations/check/
    # Body: {"item_id": "...", "location_id": "..."}
    # Runs check_reorder() live instead of just reading stored data
    @action(detail=False, methods=['post'])
    def check(self, request):
        item = Item.objects.get(id=request.data.get('item_id'))
        location = StockLocation.objects.get(id=request.data.get('location_id'))

        result = check_reorder(item, location)

        if result is None:
            return Response({'recommendation': None, 'message': 'Stock is above reorder point, no action needed.'})

        serializer = ReorderRecommendationSerializer(result)
        return Response(serializer.data)


class ABCClassificationRunViewSet(viewsets.ModelViewSet):
    queryset = ABCClassificationRun.objects.all()
    serializer_class = ABCClassificationRunSerializer

    @action(detail=False, methods=['post'])
    def run(self, request):
        results = classify_items_abc()
        serializer = ABCClassificationRunSerializer(results, many=True)
        return Response(serializer.data)


class SupplierKPIViewSet(viewsets.ModelViewSet):
    queryset = SupplierKPI.objects.all()
    serializer_class = SupplierKPISerializer


class SupplierRiskScoreViewSet(viewsets.ModelViewSet):
    queryset = SupplierRiskScore.objects.all()
    serializer_class = SupplierRiskScoreSerializer