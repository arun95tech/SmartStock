from rest_framework import serializers
from .models import ForecastRun, ReorderRecommendation, ABCClassificationRun, SupplierKPI, SupplierRiskScore


class ForecastRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastRun
        fields = '__all__'
        read_only_fields = ['id', 'generated_at']


class ReorderRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReorderRecommendation
        fields = '__all__'
        read_only_fields = ['id', 'generated_at']


class ABCClassificationRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABCClassificationRun
        fields = '__all__'


class SupplierKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierKPI
        fields = '__all__'


class SupplierRiskScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierRiskScore
        fields = '__all__'